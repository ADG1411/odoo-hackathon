# -*- coding: utf-8 -*-
"""
Maintenance Stage Model
"""
from . import db
from datetime import datetime


class MaintenanceStage(db.Model):
    """Maintenance Stage - Workflow stages for requests"""
    __tablename__ = 'maintenance_stage'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sequence = db.Column(db.Integer, default=10)
    color = db.Column(db.String(20), default='#6c757d')
    
    # Stage flags
    is_done = db.Column(db.Boolean, default=False)
    is_scrap = db.Column(db.Boolean, default=False)
    fold = db.Column(db.Boolean, default=False)
    
    # Description
    description = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('MaintenanceRequest', backref='stage', lazy='dynamic')
    
    @property
    def request_count(self):
        return self.requests.count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sequence': self.sequence,
            'color': self.color,
            'is_done': self.is_done,
            'is_scrap': self.is_scrap,
            'fold': self.fold,
            'request_count': self.request_count
        }
    
    def __repr__(self):
        return f'<MaintenanceStage {self.name}>'
