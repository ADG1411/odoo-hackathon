# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class MaintenanceRequest(models.Model):
    """Maintenance Request Model - The transactional part handling repair lifecycle"""
    _name = 'gearguard.maintenance.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, scheduled_date, id desc'
    _rec_name = 'display_name'

    # Reference Number
    reference = fields.Char(
        string='Reference',
        required=True,
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
        string='Subject',
        required=True,
        tracking=True,
        help='What is wrong? (e.g., "Leaking Oil", "Screen not working")'
    )
    active = fields.Boolean(default=True)
    description = fields.Html(string='Description')
    
    # Request Type
    request_type = fields.Selection([
        ('corrective', 'Corrective (Breakdown)'),
        ('preventive', 'Preventive (Routine Checkup)')
    ], string='Request Type', default='corrective', required=True, tracking=True,
       help='Corrective: Unplanned repair. Preventive: Planned maintenance.')
    
    # Priority
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent')
    ], string='Priority', default='1', tracking=True)
    
    # Stage and Status
    stage_id = fields.Many2one(
        'gearguard.maintenance.stage',
        string='Stage',
        tracking=True,
        group_expand='_read_group_stage_ids',
        default=lambda self: self._get_default_stage(),
        copy=False
    )
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Ready for next stage')
    ], string='Kanban State', default='normal', tracking=True)
    
    # Equipment Information
    equipment_id = fields.Many2one(
        'gearguard.equipment',
        string='Equipment',
        required=True,
        tracking=True,
        help='Which machine/asset is affected?'
    )
    category_id = fields.Many2one(
        'gearguard.equipment.category',
        string='Equipment Category',
        related='equipment_id.category_id',
        store=True,
        readonly=True
    )
    equipment_serial = fields.Char(
        string='Serial Number',
        related='equipment_id.serial_number',
        readonly=True
    )
    
    # Team and Assignment
    maintenance_team_id = fields.Many2one(
        'gearguard.maintenance.team',
        string='Maintenance Team',
        tracking=True,
        help='Team responsible for this request'
    )
    technician_id = fields.Many2one(
        'res.users',
        string='Assigned Technician',
        tracking=True,
        domain="[('id', 'in', team_member_ids)]",
        help='Technician assigned to handle this request'
    )
    team_member_ids = fields.Many2many(
        'res.users',
        compute='_compute_team_member_ids',
        string='Available Technicians'
    )
    
    # Requester Information
    request_user_id = fields.Many2one(
        'res.users',
        string='Requested By',
        default=lambda self: self.env.user,
        tracking=True
    )
    
    # Scheduling and Duration
    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.today,
        tracking=True
    )
    scheduled_date = fields.Datetime(
        string='Scheduled Date',
        tracking=True,
        help='When should the work happen?'
    )
    scheduled_date_end = fields.Datetime(
        string='Scheduled End Date',
        compute='_compute_scheduled_date_end',
        store=True
    )
    duration = fields.Float(
        string='Duration (Hours)',
        tracking=True,
        help='How long did/will the repair take?'
    )
    
    # Completion
    close_date = fields.Datetime(
        string='Close Date',
        tracking=True
    )
    hours_spent = fields.Float(
        string='Hours Spent',
        tracking=True,
        help='Actual hours spent on the repair'
    )
    
    # Overdue Logic
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_is_overdue',
        store=True
    )
    
    # Color for Kanban
    color = fields.Integer(string='Color Index')
    
    # Notes and Additional Info
    internal_notes = fields.Text(string='Internal Notes')
    resolution = fields.Text(string='Resolution', tracking=True)

    @api.model
    def _get_default_stage(self):
        """Get the default stage (New)"""
        return self.env['gearguard.maintenance.stage'].search([
            ('sequence', '=', 1)
        ], limit=1) or self.env['gearguard.maintenance.stage'].search([], limit=1)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Return all stages for Kanban view grouping"""
        return self.env['gearguard.maintenance.stage'].search([])

    @api.depends('maintenance_team_id', 'maintenance_team_id.member_ids')
    def _compute_team_member_ids(self):
        for request in self:
            if request.maintenance_team_id:
                request.team_member_ids = request.maintenance_team_id.member_ids
            else:
                request.team_member_ids = False

    @api.depends('scheduled_date', 'duration')
    def _compute_scheduled_date_end(self):
        for request in self:
            if request.scheduled_date and request.duration:
                request.scheduled_date_end = request.scheduled_date + timedelta(hours=request.duration)
            else:
                request.scheduled_date_end = request.scheduled_date

    @api.depends('scheduled_date', 'stage_id', 'stage_id.done')
    def _compute_is_overdue(self):
        now = fields.Datetime.now()
        for request in self:
            if request.scheduled_date and not request.stage_id.done:
                request.is_overdue = request.scheduled_date < now
            else:
                request.is_overdue = False

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        """Auto-fill logic: When equipment is selected, fetch team and category"""
        if self.equipment_id:
            # Auto-fill maintenance team from equipment
            if self.equipment_id.maintenance_team_id:
                self.maintenance_team_id = self.equipment_id.maintenance_team_id
            # Auto-fill default technician from equipment
            if self.equipment_id.technician_user_id:
                self.technician_id = self.equipment_id.technician_user_id

    @api.onchange('maintenance_team_id')
    def _onchange_maintenance_team_id(self):
        """Clear technician if they're not in the new team"""
        if self.maintenance_team_id:
            if self.technician_id and self.technician_id not in self.maintenance_team_id.member_ids:
                self.technician_id = False
        else:
            self.technician_id = False

    def write(self, vals):
        """Override write to handle stage changes"""
        result = super().write(vals)
        
        # Handle scrap stage logic
        if 'stage_id' in vals:
            for request in self:
                if request.stage_id.is_scrap and request.equipment_id:
                    # Mark equipment as scrapped
                    request.equipment_id.write({
                        'equipment_status': 'scrapped',
                        'scrap_date': fields.Date.today(),
                        'scrap_reason': f'Scrapped via maintenance request: {request.name}'
                    })
                    request.equipment_id.message_post(
                        body=_('Equipment scrapped due to maintenance request: %s') % request.name
                    )
                
                # Set close date when moving to done stage
                if request.stage_id.done and not request.close_date:
                    request.close_date = fields.Datetime.now()
        
        return result

    @api.depends('reference', 'name')
    def _compute_display_name(self):
        for record in self:
            if record.reference and record.reference != _('New'):
                record.display_name = f"[{record.reference}] {record.name}"
            else:
                record.display_name = record.name

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set stage and generate sequence"""
        for vals in vals_list:
            if 'stage_id' not in vals:
                vals['stage_id'] = self._get_default_stage().id
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'gearguard.maintenance.request'
                ) or _('New')
        return super().create(vals_list)

    def action_assign_to_me(self):
        """Assign the current user as technician"""
        self.ensure_one()
        if self.maintenance_team_id and self.env.user not in self.maintenance_team_id.member_ids:
            raise ValidationError(_('You are not a member of the assigned maintenance team.'))
        self.technician_id = self.env.user

    def action_start_repair(self):
        """Move request to In Progress stage"""
        in_progress_stage = self.env['gearguard.maintenance.stage'].search([
            ('name', 'ilike', 'In Progress')
        ], limit=1)
        if in_progress_stage:
            self.stage_id = in_progress_stage

    def action_mark_repaired(self):
        """Move request to Repaired stage"""
        repaired_stage = self.env['gearguard.maintenance.stage'].search([
            ('done', '=', True), ('is_scrap', '=', False)
        ], limit=1)
        if repaired_stage:
            self.write({
                'stage_id': repaired_stage.id,
                'close_date': fields.Datetime.now()
            })

    def action_scrap(self):
        """Move request to Scrap stage"""
        scrap_stage = self.env['gearguard.maintenance.stage'].search([
            ('is_scrap', '=', True)
        ], limit=1)
        if scrap_stage:
            self.stage_id = scrap_stage

    def action_send_notification(self):
        """Send email notification to assigned technician"""
        self.ensure_one()
        template = self.env.ref('gearguard.mail_template_maintenance_request_assigned', raise_if_not_found=False)
        if template and self.technician_id:
            template.send_mail(self.id, force_send=True)

    @api.model
    def _cron_check_overdue_requests(self):
        """Scheduled action to check and mark overdue requests"""
        now = fields.Datetime.now()
        overdue_requests = self.search([
            ('scheduled_date', '<', now),
            ('stage_id.done', '=', False),
            ('is_overdue', '=', False)
        ])
        overdue_requests.write({'is_overdue': True})
        
        # Send overdue notifications
        template = self.env.ref('gearguard.mail_template_maintenance_overdue', raise_if_not_found=False)
        if template:
            for request in overdue_requests:
                try:
                    template.send_mail(request.id, force_send=True)
                except Exception:
                    pass  # Don't fail if email sending fails
        
        return True

    @api.model
    def _cron_send_maintenance_reminders(self):
        """Send reminders for maintenance scheduled in the next 24 hours"""
        now = fields.Datetime.now()
        tomorrow = now + timedelta(days=1)
        
        upcoming_requests = self.search([
            ('scheduled_date', '>=', now),
            ('scheduled_date', '<=', tomorrow),
            ('stage_id.done', '=', False),
            ('technician_id', '!=', False)
        ])
        
        template = self.env.ref('gearguard.mail_template_maintenance_request_assigned', raise_if_not_found=False)
        if template:
            for request in upcoming_requests:
                try:
                    template.send_mail(request.id, force_send=True)
                except Exception:
                    pass
        
        return True

    @api.constrains('scheduled_date', 'request_type')
    def _check_scheduled_date(self):
        """Validate scheduled date for preventive maintenance"""
        for request in self:
            if request.request_type == 'preventive' and not request.scheduled_date:
                raise ValidationError(_('Preventive maintenance requests must have a scheduled date.'))

    @api.constrains('hours_spent')
    def _check_hours_spent(self):
        """Validate hours spent"""
        for request in self:
            if request.hours_spent < 0:
                raise ValidationError(_('Hours spent cannot be negative.'))
