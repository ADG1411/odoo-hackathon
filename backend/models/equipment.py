# -*- coding: utf-8 -*-
"""
Equipment Model
"""
from . import db
from datetime import datetime


class Equipment(db.Model):
    """Equipment - Assets that need maintenance"""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('equipment_category.id'))
    
    # Details
    serial_number = db.Column(db.String(100))
    model = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    
    # Location & Assignment
    location = db.Column(db.String(200))
    department = db.Column(db.String(100))
    owner_name = db.Column(db.String(100))
    owner_email = db.Column(db.String(100))
    
    # Default Maintenance Assignment (Auto-fill logic)
    default_team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'))
    default_technician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Status: operational, maintenance, broken, scrapped
    status = db.Column(db.String(20), default='operational')
    
    # Dates
    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)
    last_maintenance = db.Column(db.Date)
    next_maintenance = db.Column(db.Date)
    
    # Additional
    cost = db.Column(db.Numeric(12, 2))
    notes = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    
    # Scrap tracking
    is_scrapped = db.Column(db.Boolean, default=False)
    scrap_date = db.Column(db.Date)
    scrap_reason = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    maintenance_requests = db.relationship('MaintenanceRequest', backref='equipment', lazy='dynamic')
    default_team = db.relationship('MaintenanceTeam', foreign_keys=[default_team_id])
    default_technician = db.relationship('User', foreign_keys=[default_technician_id])
    
    @staticmethod
    def generate_code():
        """Generate next equipment code EQ-0001, EQ-0002..."""
        last = Equipment.query.order_by(Equipment.id.desc()).first()
        if last:
            num = int(last.code.split('-')[1]) + 1
        else:
            num = 1
        return f'EQ-{num:04d}'
    
    @property
    def is_warranty_valid(self):
        if not self.warranty_expiry:
            return False
        return self.warranty_expiry >= datetime.now().date()
    
    @property
    def status_color(self):
        colors = {
            'operational': 'success',
            'maintenance': 'warning',
            'broken': 'danger',
            'scrapped': 'secondary'
        }
        return colors.get(self.status, 'secondary')
    
    @property
    def open_request_count(self):
        """Count of open (non-completed) maintenance requests"""
        from .maintenance_stage import MaintenanceStage
        return self.maintenance_requests.join(MaintenanceStage).filter(
            MaintenanceStage.is_done == False,
            MaintenanceStage.is_scrap == False
        ).count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'serial_number': self.serial_number,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'location': self.location,
            'department': self.department,
            'owner_name': self.owner_name,
            'owner_email': self.owner_email,
            'default_team_id': self.default_team_id,
            'default_team_name': self.default_team.name if self.default_team else None,
            'default_technician_id': self.default_technician_id,
            'default_technician_name': self.default_technician.full_name if self.default_technician else None,
            'status': self.status,
            'status_color': self.status_color,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'warranty_expiry': self.warranty_expiry.isoformat() if self.warranty_expiry else None,
            'is_warranty_valid': self.is_warranty_valid,
            'last_maintenance': self.last_maintenance.isoformat() if self.last_maintenance else None,
            'next_maintenance': self.next_maintenance.isoformat() if self.next_maintenance else None,
            'cost': float(self.cost) if self.cost else None,
            'notes': self.notes,
            'is_scrapped': self.is_scrapped,
            'scrap_date': self.scrap_date.isoformat() if self.scrap_date else None,
            'scrap_reason': self.scrap_reason,
            'request_count': self.maintenance_requests.count(),
            'open_request_count': self.open_request_count
        }
    
    def __repr__(self):
        return f'<Equipment {self.code} - {self.name}>'
