# -*- coding: utf-8 -*-
{
    'name': 'GearGuard - Maintenance Tracker',
    'version': '17.0.1.0.0',
    'category': 'Maintenance',
    'summary': 'The Ultimate Maintenance Management System',
    'description': """
GearGuard: The Ultimate Maintenance Tracker
============================================

A comprehensive maintenance management system that allows companies to:
- Track assets (machines, vehicles, computers)
- Manage maintenance requests for those assets
- Connect Equipment, Teams, and Requests seamlessly

Key Features:
- Equipment tracking by department and employee
- Multiple specialized maintenance teams
- Corrective and Preventive maintenance requests
- Kanban board with drag & drop
- Calendar view for scheduled maintenance
- Smart buttons and automated workflows
    """,
    'author': 'GearGuard Team',
    'website': 'https://github.com/ADG1411/odoo-hackathon',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/gearguard_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/stage_data.xml',
        'data/mail_template_data.xml',
        'data/cron_data.xml',
        'views/equipment_category_views.xml',
        'views/equipment_views.xml',
        'views/maintenance_team_views.xml',
        'views/maintenance_request_views.xml',
        'views/maintenance_stage_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gearguard/static/src/css/gearguard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
