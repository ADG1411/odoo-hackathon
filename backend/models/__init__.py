# -*- coding: utf-8 -*-
"""
GearGuard - Database Models
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .equipment_category import EquipmentCategory
from .equipment import Equipment
from .maintenance_team import MaintenanceTeam, TeamMember
from .maintenance_stage import MaintenanceStage
from .maintenance_request import MaintenanceRequest
from .user import User, Role, ActivityLog
from .technician import Technician, SKILL_TYPES, AVAILABILITY_STATUSES

__all__ = [
    'db',
    'EquipmentCategory',
    'Equipment',
    'MaintenanceTeam',
    'TeamMember',
    'MaintenanceStage',
    'MaintenanceRequest',
    'User',
    'Role',
    'ActivityLog',
    'Technician',
    'SKILL_TYPES',
    'AVAILABILITY_STATUSES'
]
