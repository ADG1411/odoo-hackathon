# -*- coding: utf-8 -*-
"""
Maintenance Request Model
"""
from . import db
from datetime import datetime


class MaintenanceRequest(db.Model):
    """Maintenance Request - Core entity for tracking maintenance"""
    __tablename__ = 'maintenance_request'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Relations
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'))
    stage_id = db.Column(db.Integer, db.ForeignKey('maintenance_stage.id'))
    
    # Request details
    request_type = db.Column(db.String(20), default='corrective')  # corrective, preventive
    priority = db.Column(db.String(10), default='normal')  # low, normal, high, urgent
    
    # Requester info
    requester_name = db.Column(db.String(100))
    requester_email = db.Column(db.String(100))
    requester_phone = db.Column(db.String(20))
    
    # Dates
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    
    # Duration & Cost
    duration_hours = db.Column(db.Numeric(6, 2))
    maintenance_cost = db.Column(db.Numeric(12, 2))
    
    # Notes
    technician_notes = db.Column(db.Text)
    resolution = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def generate_reference():
        """Generate next reference MR-00001, MR-00002..."""
        last = MaintenanceRequest.query.order_by(MaintenanceRequest.id.desc()).first()
        if last:
            num = int(last.reference.split('-')[1]) + 1
        else:
            num = 1
        return f'MR-{num:05d}'
    
    @property
    def is_overdue(self):
        if not self.deadline:
            return False
        if self.stage and (self.stage.is_done or self.stage.is_scrap):
            return False
        return self.deadline < datetime.utcnow()
    
    @property
    def priority_color(self):
        colors = {
            'low': 'secondary',
            'normal': 'info',
            'high': 'warning',
            'urgent': 'danger'
        }
        return colors.get(self.priority, 'info')
    
    @property
    def priority_icon(self):
        icons = {
            'low': 'bi-arrow-down',
            'normal': 'bi-dash',
            'high': 'bi-arrow-up',
            'urgent': 'bi-exclamation-triangle-fill'
        }
        return icons.get(self.priority, 'bi-dash')
    
    @property
    def type_icon(self):
        return 'bi-wrench' if self.request_type == 'corrective' else 'bi-calendar-check'
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'name': self.name,
            'description': self.description,
            'equipment_id': self.equipment_id,
            'equipment_name': self.equipment.name if self.equipment else None,
            'equipment_code': self.equipment.code if self.equipment else None,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'stage_id': self.stage_id,
            'stage_name': self.stage.name if self.stage else None,
            'stage_color': self.stage.color if self.stage else '#6c757d',
            'request_type': self.request_type,
            'priority': self.priority,
            'priority_color': self.priority_color,
            'requester_name': self.requester_name,
            'requester_email': self.requester_email,
            'request_date': self.request_date.isoformat() if self.request_date else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'is_overdue': self.is_overdue,
            'duration_hours': float(self.duration_hours) if self.duration_hours else None,
            'maintenance_cost': float(self.maintenance_cost) if self.maintenance_cost else None,
            'resolution': self.resolution
        }
    
    def __repr__(self):
        return f'<MaintenanceRequest {self.reference}>'
