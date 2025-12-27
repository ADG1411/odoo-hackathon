# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceStage(models.Model):
    """Maintenance Request Stage Model"""
    _name = 'gearguard.maintenance.stage'
    _description = 'Maintenance Request Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    fold = fields.Boolean(
        string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.'
    )
    done = fields.Boolean(
        string='Request Done',
        help='Requests in this stage are considered as done.'
    )
    is_scrap = fields.Boolean(
        string='Scrap Stage',
        help='If checked, moving a request to this stage will mark the equipment as scrapped.'
    )
    
    # Visual
    color = fields.Integer(string='Color Index')
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Stage name must be unique!')
    ]
