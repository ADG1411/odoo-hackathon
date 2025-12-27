# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EquipmentCategory(models.Model):
    """Equipment Category Model for categorizing equipment types"""
    _name = 'gearguard.equipment.category'
    _description = 'Equipment Category'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color Index')
    
    # Related fields
    equipment_ids = fields.One2many(
        'gearguard.equipment', 
        'category_id', 
        string='Equipment'
    )
    equipment_count = fields.Integer(
        string='Equipment Count',
        compute='_compute_equipment_count'
    )
    
    # Default maintenance team for this category
    maintenance_team_id = fields.Many2one(
        'gearguard.maintenance.team',
        string='Default Maintenance Team',
        help='Default team responsible for maintaining equipment in this category'
    )

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for category in self:
            category.equipment_count = len(category.equipment_ids)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Category name must be unique!')
    ]
