# -*- coding: utf-8 -*-
"""
Technician Model - Modern Industrial SaaS
"""
from . import db
from datetime import datetime


class Technician(db.Model):
    """Technician - Skilled workers for maintenance operations"""
    __tablename__ = 'technician'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Skill / Specialization
    skill = db.Column(db.String(100), nullable=False, default='General')
    
    # Team assignment
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'), nullable=True)
    
    # Company
    company_name = db.Column(db.String(100))
    
    # Availability Status: available, busy, off_duty
    availability_status = db.Column(db.String(20), default='available')
    
    # Contact info (optional)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Avatar color for initials display
    avatar_color = db.Column(db.String(20), default='#6366f1')
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    team = db.relationship('MaintenanceTeam', backref=db.backref('technicians', lazy='dynamic'))
    
    @property
    def initials(self):
        """Generate initials from name"""
        parts = self.name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return self.name[:2].upper()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'skill': self.skill,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'company_name': self.company_name,
            'availability_status': self.availability_status,
            'email': self.email,
            'phone': self.phone,
            'avatar_color': self.avatar_color,
            'initials': self.initials,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Technician {self.name}>'


# Predefined skill types for consistency
SKILL_TYPES = [
    'Electrical',
    'Mechanical',
    'HVAC',
    'Plumbing',
    'General',
    'Welding',
    'Automation',
    'Instrumentation',
    'Civil',
    'Safety'
]

# Availability statuses
AVAILABILITY_STATUSES = [
    ('available', 'Available'),
    ('busy', 'Busy'),
    ('off_duty', 'Off-duty')
]
