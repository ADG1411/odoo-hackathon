# -*- coding: utf-8 -*-
"""
Maintenance Team Model
"""
from . import db
from datetime import datetime


class MaintenanceTeam(db.Model):
    """Maintenance Team - Groups of technicians"""
    __tablename__ = 'maintenance_team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(20), default='#0d6efd')
    
    # Leader
    leader_name = db.Column(db.String(100))
    leader_email = db.Column(db.String(100))
    leader_phone = db.Column(db.String(20))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy='dynamic', cascade='all, delete-orphan')
    maintenance_requests = db.relationship('MaintenanceRequest', backref='team', lazy='dynamic')
    equipment = db.relationship('Equipment', foreign_keys='Equipment.default_team_id', backref='assigned_team', lazy='dynamic', viewonly=True)
    
    @property
    def member_count(self):
        return self.members.count()
    
    @property
    def open_requests_count(self):
        return self.maintenance_requests.join(MaintenanceRequest.stage).filter(
            db.not_(db.or_(
                MaintenanceStage.is_done == True,
                MaintenanceStage.is_scrap == True
            ))
        ).count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'leader_name': self.leader_name,
            'leader_email': self.leader_email,
            'leader_phone': self.leader_phone,
            'is_active': self.is_active,
            'member_count': self.member_count,
            'members': [m.to_dict() for m in self.members]
        }
    
    def __repr__(self):
        return f'<MaintenanceTeam {self.name}>'


class TeamMember(db.Model):
    """Team Member - Technicians in a team"""
    __tablename__ = 'team_member'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='Technician')
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<TeamMember {self.name}>'


# Import at bottom to avoid circular imports
from .maintenance_stage import MaintenanceStage
