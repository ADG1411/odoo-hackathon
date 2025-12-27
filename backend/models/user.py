# -*- coding: utf-8 -*-
"""
User Model with Role-Based Access Control
"""
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    """User Roles - Admin, Manager, Technician, User"""
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    # Permissions (booleans for simplicity)
    can_manage_users = db.Column(db.Boolean, default=False)
    can_manage_teams = db.Column(db.Boolean, default=False)
    can_manage_equipment = db.Column(db.Boolean, default=False)
    can_manage_requests = db.Column(db.Boolean, default=False)
    can_manage_settings = db.Column(db.Boolean, default=False)
    can_view_reports = db.Column(db.Boolean, default=False)
    can_assign_requests = db.Column(db.Boolean, default=False)
    can_complete_requests = db.Column(db.Boolean, default=False)
    
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': {
                'can_manage_users': self.can_manage_users,
                'can_manage_teams': self.can_manage_teams,
                'can_manage_equipment': self.can_manage_equipment,
                'can_manage_requests': self.can_manage_requests,
                'can_manage_settings': self.can_manage_settings,
                'can_view_reports': self.can_view_reports,
                'can_assign_requests': self.can_assign_requests,
                'can_complete_requests': self.can_complete_requests,
            }
        }
    
    @staticmethod
    def create_default_roles():
        """Create default roles if they don't exist"""
        roles = [
            {
                'name': 'Admin',
                'description': 'Full system access',
                'can_manage_users': True,
                'can_manage_teams': True,
                'can_manage_equipment': True,
                'can_manage_requests': True,
                'can_manage_settings': True,
                'can_view_reports': True,
                'can_assign_requests': True,
                'can_complete_requests': True,
            },
            {
                'name': 'Manager',
                'description': 'Can manage teams and view reports',
                'can_manage_users': False,
                'can_manage_teams': True,
                'can_manage_equipment': True,
                'can_manage_requests': True,
                'can_manage_settings': False,
                'can_view_reports': True,
                'can_assign_requests': True,
                'can_complete_requests': True,
            },
            {
                'name': 'Technician',
                'description': 'Can work on assigned requests',
                'can_manage_users': False,
                'can_manage_teams': False,
                'can_manage_equipment': False,
                'can_manage_requests': False,
                'can_manage_settings': False,
                'can_view_reports': False,
                'can_assign_requests': False,
                'can_complete_requests': True,
            },
            {
                'name': 'User',
                'description': 'Can create and view requests',
                'can_manage_users': False,
                'can_manage_teams': False,
                'can_manage_equipment': False,
                'can_manage_requests': False,
                'can_manage_settings': False,
                'can_view_reports': False,
                'can_assign_requests': False,
                'can_complete_requests': False,
            },
        ]
        
        for role_data in roles:
            if not Role.query.filter_by(name=role_data['name']).first():
                role = Role(**role_data)
                db.session.add(role)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Profile
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(500))
    
    # Role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
    # Team association (for technicians)
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    team = db.relationship('MaintenanceTeam', foreign_keys=[team_id], backref='team_users')
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        if not self.role:
            return False
        return getattr(self.role, permission, False)
    
    def is_admin(self):
        return self.role and self.role.name == 'Admin'
    
    def is_manager(self):
        return self.role and self.role.name in ['Admin', 'Manager']
    
    def is_technician(self):
        return self.role and self.role.name in ['Admin', 'Manager', 'Technician']
    
    def to_dict(self, include_role=True):
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'team_id': self.team_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        if include_role and self.role:
            data['role'] = self.role.to_dict()
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'


class ActivityLog(db.Model):
    """Track user activities for audit"""
    __tablename__ = 'activity_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(50), nullable=False)  # create, update, delete, login, logout
    entity_type = db.Column(db.String(50))  # equipment, request, team, etc.
    entity_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activities')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
