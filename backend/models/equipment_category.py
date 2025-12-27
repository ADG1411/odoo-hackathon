# -*- coding: utf-8 -*-
"""
Equipment Category Model
"""
from . import db
from datetime import datetime


class EquipmentCategory(db.Model):
    """Equipment Category - Groups similar equipment types"""
    __tablename__ = 'equipment_category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(20), default='#6c757d')
    icon = db.Column(db.String(50), default='bi-box')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    equipment = db.relationship('Equipment', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'icon': self.icon,
            'equipment_count': self.equipment.count()
        }
    
    def __repr__(self):
        return f'<EquipmentCategory {self.name}>'
