# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceTeam(models.Model):
    """Maintenance Team Model for organizing technicians"""
    _name = 'gearguard.maintenance.team'
    _description = 'Maintenance Team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(
        string='Team Name', 
        required=True, 
        tracking=True,
        help='Name of the maintenance team (e.g., Mechanics, Electricians, IT Support)'
    )
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    color = fields.Integer(string='Color Index')
    
    # Team Members
    member_ids = fields.Many2many(
        'res.users',
        'gearguard_team_member_rel',
        'team_id',
        'user_id',
        string='Team Members',
        help='Users (Technicians) who belong to this team'
    )
    team_leader_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        tracking=True,
        domain="[('id', 'in', member_ids)]",
        help='Leader of the maintenance team'
    )
    
    # Related fields
    equipment_ids = fields.One2many(
        'gearguard.equipment',
        'maintenance_team_id',
        string='Equipment'
    )
    equipment_count = fields.Integer(
        string='Equipment Count',
        compute='_compute_equipment_count'
    )
    
    request_ids = fields.One2many(
        'gearguard.maintenance.request',
        'maintenance_team_id',
        string='Maintenance Requests'
    )
    request_count = fields.Integer(
        string='Request Count',
        compute='_compute_request_count'
    )
    open_request_count = fields.Integer(
        string='Open Requests',
        compute='_compute_request_count'
    )
    
    # Description
    description = fields.Text(string='Description')
    specialty = fields.Char(
        string='Specialty',
        help='Team specialty (e.g., Mechanical, Electrical, IT)'
    )

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for team in self:
            team.equipment_count = len(team.equipment_ids)

    @api.depends('request_ids', 'request_ids.stage_id')
    def _compute_request_count(self):
        for team in self:
            requests = team.request_ids
            team.request_count = len(requests)
            team.open_request_count = len(
                requests.filtered(lambda r: r.stage_id.done != True)
            )

    def action_view_requests(self):
        """Open list of maintenance requests for this team"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Requests - {self.name}',
            'res_model': 'gearguard.maintenance.request',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph',
            'domain': [('maintenance_team_id', '=', self.id)],
            'context': {
                'default_maintenance_team_id': self.id,
            },
        }

    def action_view_equipment(self):
        """Open list of equipment for this team"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Equipment - {self.name}',
            'res_model': 'gearguard.equipment',
            'view_mode': 'tree,form',
            'domain': [('maintenance_team_id', '=', self.id)],
            'context': {
                'default_maintenance_team_id': self.id,
            },
        }

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Team name must be unique!')
    ]
