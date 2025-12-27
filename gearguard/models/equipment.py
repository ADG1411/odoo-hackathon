# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Equipment(models.Model):
    """Equipment Model for tracking company assets"""
    _name = 'gearguard.equipment'
    _description = 'Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'display_name'

    # Reference/Code
    code = fields.Char(
        string='Equipment Code',
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )

    # Basic Information
    name = fields.Char(
        string='Equipment Name', 
        required=True, 
        tracking=True,
        help='Name of the equipment/asset'
    )
    serial_number = fields.Char(
        string='Serial Number',
        tracking=True,
        help='Unique serial number of the equipment'
    )
    active = fields.Boolean(default=True, tracking=True)
    image = fields.Binary(string='Image')
    note = fields.Html(string='Internal Notes')
    
    # Category and Classification
    category_id = fields.Many2one(
        'gearguard.equipment.category',
        string='Category',
        tracking=True,
        help='Equipment category (e.g., Machinery, Vehicle, Computer)'
    )
    
    # Purchase and Warranty Information
    purchase_date = fields.Date(
        string='Purchase Date',
        tracking=True
    )
    purchase_value = fields.Float(
        string='Purchase Value',
        tracking=True
    )
    warranty_expiration_date = fields.Date(
        string='Warranty Expiration',
        tracking=True
    )
    warranty_status = fields.Selection([
        ('valid', 'Under Warranty'),
        ('expired', 'Warranty Expired'),
        ('none', 'No Warranty')
    ], string='Warranty Status', compute='_compute_warranty_status', store=True)
    
    # Location Information
    location = fields.Char(
        string='Location',
        tracking=True,
        help='Physical location of the equipment (e.g., Building A, Floor 2)'
    )
    
    # Ownership - Department
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        tracking=True,
        help='Department that owns this equipment'
    )
    
    # Ownership - Employee
    employee_id = fields.Many2one(
        'hr.employee',
        string='Assigned Employee',
        tracking=True,
        help='Employee responsible for this equipment'
    )
    owner_user_id = fields.Many2one(
        'res.users',
        string='Owner',
        tracking=True,
        help='User who owns this equipment'
    )
    
    # Maintenance Responsibility
    maintenance_team_id = fields.Many2one(
        'gearguard.maintenance.team',
        string='Maintenance Team',
        tracking=True,
        help='Team responsible for maintaining this equipment'
    )
    technician_user_id = fields.Many2one(
        'res.users',
        string='Default Technician',
        tracking=True,
        domain="[('id', 'in', team_member_ids)]",
        help='Default technician assigned to this equipment'
    )
    team_member_ids = fields.Many2many(
        'res.users',
        compute='_compute_team_member_ids',
        string='Team Members'
    )
    
    # Equipment Status
    equipment_status = fields.Selection([
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('scrapped', 'Scrapped'),
    ], string='Status', default='operational', tracking=True)
    scrap_date = fields.Date(string='Scrap Date', tracking=True)
    scrap_reason = fields.Text(string='Scrap Reason')
    
    # Maintenance Request Related
    maintenance_request_ids = fields.One2many(
        'gearguard.maintenance.request',
        'equipment_id',
        string='Maintenance Requests'
    )
    maintenance_count = fields.Integer(
        string='Maintenance Count',
        compute='_compute_maintenance_count'
    )
    open_maintenance_count = fields.Integer(
        string='Open Maintenance Count',
        compute='_compute_maintenance_count'
    )
    
    # Technical Information
    model = fields.Char(string='Model')
    manufacturer = fields.Char(string='Manufacturer')
    specifications = fields.Text(string='Technical Specifications')

    @api.depends('warranty_expiration_date')
    def _compute_warranty_status(self):
        today = fields.Date.today()
        for equipment in self:
            if not equipment.warranty_expiration_date:
                equipment.warranty_status = 'none'
            elif equipment.warranty_expiration_date >= today:
                equipment.warranty_status = 'valid'
            else:
                equipment.warranty_status = 'expired'

    @api.depends('maintenance_team_id', 'maintenance_team_id.member_ids')
    def _compute_team_member_ids(self):
        for equipment in self:
            if equipment.maintenance_team_id:
                equipment.team_member_ids = equipment.maintenance_team_id.member_ids
            else:
                equipment.team_member_ids = False

    @api.depends('maintenance_request_ids', 'maintenance_request_ids.stage_id')
    def _compute_maintenance_count(self):
        for equipment in self:
            requests = equipment.maintenance_request_ids
            equipment.maintenance_count = len(requests)
            equipment.open_maintenance_count = len(
                requests.filtered(lambda r: r.stage_id.done != True)
            )

    @api.onchange('category_id')
    def _onchange_category_id(self):
        """Auto-fill maintenance team from category"""
        if self.category_id and self.category_id.maintenance_team_id:
            self.maintenance_team_id = self.category_id.maintenance_team_id

    @api.onchange('maintenance_team_id')
    def _onchange_maintenance_team_id(self):
        """Reset technician when team changes"""
        if self.maintenance_team_id:
            # Set first team member as default technician if available
            if self.maintenance_team_id.member_ids:
                self.technician_user_id = self.maintenance_team_id.member_ids[0]
            else:
                self.technician_user_id = False
        else:
            self.technician_user_id = False

    def action_view_maintenance_requests(self):
        """Open list of maintenance requests for this equipment"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Maintenance Requests - {self.name}',
            'res_model': 'gearguard.maintenance.request',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph',
            'domain': [('equipment_id', '=', self.id)],
            'context': {
                'default_equipment_id': self.id,
                'default_maintenance_team_id': self.maintenance_team_id.id if self.maintenance_team_id else False,
                'default_technician_id': self.technician_user_id.id if self.technician_user_id else False,
            },
        }

    def action_scrap_equipment(self):
        """Mark equipment as scrapped"""
        self.ensure_one()
        self.write({
            'equipment_status': 'scrapped',
            'scrap_date': fields.Date.today(),
            'active': False,
        })
        self.message_post(body=_('Equipment has been scrapped and marked as inactive.'))
        return True

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            if record.code and record.code != _('New'):
                record.display_name = f"[{record.code}] {record.name}"
            else:
                record.display_name = record.name

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to generate equipment code"""
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'gearguard.equipment'
                ) or _('New')
        return super().create(vals_list)

    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        """Validate purchase value"""
        for equipment in self:
            if equipment.purchase_value < 0:
                raise ValidationError(_('Purchase value cannot be negative.'))

    _sql_constraints = [
        ('serial_unique', 'UNIQUE(serial_number)', 'Serial number must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'Equipment code must be unique!')
    ]
