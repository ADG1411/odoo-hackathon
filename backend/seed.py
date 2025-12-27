# -*- coding: utf-8 -*-
"""
GearGuard - Seed Data
"""
from backend.models import db, EquipmentCategory, Equipment, MaintenanceTeam, TeamMember, MaintenanceStage, MaintenanceRequest, User, Role
from datetime import datetime, timedelta
import random


def seed_database():
    """Populate database with demo data"""
    print("🌱 Starting database seed...")
    
    # Clear existing data
    print("  Clearing existing data...")
    MaintenanceRequest.query.delete()
    TeamMember.query.delete()
    MaintenanceTeam.query.delete()
    Equipment.query.delete()
    EquipmentCategory.query.delete()
    MaintenanceStage.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Ensure roles exist
    Role.create_default_roles()
    
    # ==================== USERS ====================
    print("  Creating users...")
    admin_role = Role.query.filter_by(name='Admin').first()
    manager_role = Role.query.filter_by(name='Manager').first()
    tech_role = Role.query.filter_by(name='Technician').first()
    user_role = Role.query.filter_by(name='User').first()
    
    users_data = [
        {'email': 'admin@gearguard.com', 'first_name': 'System', 'last_name': 'Admin', 'role': admin_role, 'password': 'admin123'},
        {'email': 'abhi.gabani@gearguard.com', 'first_name': 'Gabani Abhi', 'last_name': 'Dineshbhai', 'role': manager_role, 'password': 'password123'},
        {'email': 'preet.k@gearguard.com', 'first_name': 'Preet', 'last_name': 'Kakdiya', 'role': tech_role, 'password': 'password123'},
        {'email': 'tirth.g@gearguard.com', 'first_name': 'Tirth', 'last_name': 'Goyani', 'role': tech_role, 'password': 'password123'},
        {'email': 'rajesh.p@gearguard.com', 'first_name': 'Rajesh', 'last_name': 'Patel', 'role': manager_role, 'password': 'password123'},
        {'email': 'user@gearguard.com', 'first_name': 'Demo', 'last_name': 'User', 'role': user_role, 'password': 'user123'},
    ]
    
    users = {}
    for data in users_data:
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role_id=data['role'].id if data['role'] else None
        )
        user.set_password(data['password'])
        db.session.add(user)
        users[data['email']] = user
    db.session.commit()
    
    # ==================== STAGES ====================
    print("  Creating stages...")
    stages_data = [
        {'name': 'New', 'sequence': 10, 'color': '#6c757d', 'is_done': False, 'is_scrap': False, 'fold': False},
        {'name': 'In Progress', 'sequence': 20, 'color': '#0d6efd', 'is_done': False, 'is_scrap': False, 'fold': False},
        {'name': 'Waiting Parts', 'sequence': 30, 'color': '#ffc107', 'is_done': False, 'is_scrap': False, 'fold': False},
        {'name': 'Under Review', 'sequence': 40, 'color': '#17a2b8', 'is_done': False, 'is_scrap': False, 'fold': False},
        {'name': 'Completed', 'sequence': 50, 'color': '#28a745', 'is_done': True, 'is_scrap': False, 'fold': True},
        {'name': 'Scrapped', 'sequence': 60, 'color': '#dc3545', 'is_done': False, 'is_scrap': True, 'fold': True},
    ]
    
    stages = {}
    for data in stages_data:
        stage = MaintenanceStage(**data)
        db.session.add(stage)
        stages[data['name']] = stage
    db.session.commit()
    
    # ==================== CATEGORIES ====================
    print("  Creating categories...")
    categories_data = [
        {'name': 'Computers & Laptops', 'description': 'Desktop computers, laptops, workstations', 'color': '#0d6efd', 'icon': 'bi-laptop'},
        {'name': 'Vehicles', 'description': 'Cars, trucks, forklifts, company vehicles', 'color': '#198754', 'icon': 'bi-truck'},
        {'name': 'Production Machines', 'description': 'Manufacturing and production equipment', 'color': '#dc3545', 'icon': 'bi-gear'},
        {'name': 'HVAC Systems', 'description': 'Heating, ventilation, air conditioning', 'color': '#0dcaf0', 'icon': 'bi-thermometer-half'},
        {'name': 'Office Equipment', 'description': 'Printers, copiers, projectors', 'color': '#6f42c1', 'icon': 'bi-printer'},
        {'name': 'Safety Equipment', 'description': 'Fire extinguishers, alarms, safety gear', 'color': '#fd7e14', 'icon': 'bi-shield-check'},
    ]
    
    categories = {}
    for data in categories_data:
        cat = EquipmentCategory(**data)
        db.session.add(cat)
        categories[data['name']] = cat
    db.session.commit()
    
    # ==================== TEAMS ====================
    print("  Creating teams...")
    teams_data = [
        {
            'name': 'IT Support Team',
            'description': 'Handles all IT related maintenance including computers, networks, and software',
            'color': '#0d6efd',
            'leader_name': 'Gabani Abhi Dineshbhai',
            'leader_email': 'abhi.gabani@gearguard.com',
            'leader_phone': '+91 98765 43210',
            'members': [
                {'name': 'Preet Kakdiya', 'email': 'preet.k@gearguard.com', 'role': 'Senior Technician'},
                {'name': 'Tirth Goyani', 'email': 'tirth.g@gearguard.com', 'role': 'Technician'},
            ]
        },
        {
            'name': 'Mechanical Team',
            'description': 'Production machines, vehicles, and mechanical equipment maintenance',
            'color': '#dc3545',
            'leader_name': 'Rajesh Patel',
            'leader_email': 'rajesh.p@gearguard.com',
            'leader_phone': '+91 98765 43211',
            'members': [
                {'name': 'Amit Shah', 'email': 'amit.s@gearguard.com', 'role': 'Senior Mechanic'},
                {'name': 'Vijay Kumar', 'email': 'vijay.k@gearguard.com', 'role': 'Mechanic'},
                {'name': 'Suresh Joshi', 'email': 'suresh.j@gearguard.com', 'role': 'Mechanic'},
            ]
        },
        {
            'name': 'Facilities Team',
            'description': 'Building maintenance, HVAC, electrical, and general facilities',
            'color': '#198754',
            'leader_name': 'Nilesh Sharma',
            'leader_email': 'nilesh.s@gearguard.com',
            'leader_phone': '+91 98765 43212',
            'members': [
                {'name': 'Prakash Dave', 'email': 'prakash.d@gearguard.com', 'role': 'Electrician'},
                {'name': 'Mahesh Trivedi', 'email': 'mahesh.t@gearguard.com', 'role': 'HVAC Technician'},
            ]
        },
    ]
    
    teams = {}
    for data in teams_data:
        members_data = data.pop('members')
        team = MaintenanceTeam(**data)
        db.session.add(team)
        db.session.flush()
        
        for member_data in members_data:
            member = TeamMember(team_id=team.id, **member_data)
            db.session.add(member)
        
        teams[team.name] = team
    db.session.commit()
    
    # ==================== EQUIPMENT ====================
    print("  Creating equipment...")
    
    # Get technician users for default assignments
    tech_preet = users.get('preet.k@gearguard.com')
    tech_tirth = users.get('tirth.g@gearguard.com')
    
    equipment_data = [
        # Computers - Assigned to IT Support Team
        {'name': 'Dell OptiPlex 7090', 'category': 'Computers & Laptops', 'location': 'Office Floor 1', 'department': 'Engineering', 'owner_name': 'John Doe', 'status': 'operational', 'manufacturer': 'Dell', 'model': 'OptiPlex 7090', 'default_team': 'IT Support Team', 'default_tech': tech_preet},
        {'name': 'HP EliteBook 840 G8', 'category': 'Computers & Laptops', 'location': 'Office Floor 2', 'department': 'Sales', 'owner_name': 'Jane Smith', 'status': 'operational', 'manufacturer': 'HP', 'model': 'EliteBook 840 G8', 'default_team': 'IT Support Team', 'default_tech': tech_tirth},
        {'name': 'MacBook Pro 16"', 'category': 'Computers & Laptops', 'location': 'Design Studio', 'department': 'Design', 'owner_name': 'Mike Wilson', 'status': 'maintenance', 'manufacturer': 'Apple', 'model': 'MacBook Pro 16', 'default_team': 'IT Support Team', 'default_tech': tech_preet},
        {'name': 'Dell PowerEdge R740', 'category': 'Computers & Laptops', 'location': 'Server Room', 'department': 'IT', 'owner_name': 'IT Department', 'status': 'operational', 'manufacturer': 'Dell', 'model': 'PowerEdge R740', 'default_team': 'IT Support Team', 'default_tech': tech_tirth},
        
        # Vehicles - Assigned to Mechanical Team
        {'name': 'Toyota Innova Crysta', 'category': 'Vehicles', 'location': 'Parking Lot A', 'department': 'Admin', 'owner_name': 'Company Pool', 'status': 'operational', 'manufacturer': 'Toyota', 'model': 'Innova Crysta', 'default_team': 'Mechanical Team', 'default_tech': None},
        {'name': 'Maruti Suzuki Swift', 'category': 'Vehicles', 'location': 'Parking Lot B', 'department': 'Sales', 'owner_name': 'Sales Team', 'status': 'operational', 'manufacturer': 'Maruti Suzuki', 'model': 'Swift', 'default_team': 'Mechanical Team', 'default_tech': None},
        {'name': 'Toyota Forklift 8FBN25', 'category': 'Vehicles', 'location': 'Warehouse', 'department': 'Logistics', 'owner_name': 'Warehouse Team', 'status': 'maintenance', 'manufacturer': 'Toyota', 'model': '8FBN25', 'default_team': 'Mechanical Team', 'default_tech': None},
        
        # Production Machines - Assigned to Mechanical Team
        {'name': 'CNC Milling Machine', 'category': 'Production Machines', 'location': 'Production Floor', 'department': 'Production', 'owner_name': 'Production Team', 'status': 'operational', 'manufacturer': 'Haas', 'model': 'VF-2', 'default_team': 'Mechanical Team', 'default_tech': None},
        {'name': 'Laser Cutting Machine', 'category': 'Production Machines', 'location': 'Production Floor', 'department': 'Production', 'owner_name': 'Production Team', 'status': 'operational', 'manufacturer': 'Trumpf', 'model': 'TruLaser 3030', 'default_team': 'Mechanical Team', 'default_tech': None},
        {'name': 'Industrial Robot Arm', 'category': 'Production Machines', 'location': 'Assembly Line', 'department': 'Production', 'owner_name': 'Production Team', 'status': 'broken', 'manufacturer': 'ABB', 'model': 'IRB 6700', 'default_team': 'Mechanical Team', 'default_tech': None},
        
        # HVAC - Assigned to Facilities Team
        {'name': 'Central AC Unit - Building A', 'category': 'HVAC Systems', 'location': 'Rooftop', 'department': 'Facilities', 'owner_name': 'Facilities Team', 'status': 'operational', 'manufacturer': 'Daikin', 'model': 'VRV IV', 'default_team': 'Facilities Team', 'default_tech': None},
        {'name': 'Split AC - Conference Room', 'category': 'HVAC Systems', 'location': 'Floor 2', 'department': 'Facilities', 'owner_name': 'Facilities Team', 'status': 'operational', 'manufacturer': 'LG', 'model': 'Dual Inverter', 'default_team': 'Facilities Team', 'default_tech': None},
        
        # Office Equipment - Assigned to IT Support Team
        {'name': 'HP LaserJet Enterprise', 'category': 'Office Equipment', 'location': 'Print Room', 'department': 'Admin', 'owner_name': 'Admin Team', 'status': 'operational', 'manufacturer': 'HP', 'model': 'LaserJet M607', 'default_team': 'IT Support Team', 'default_tech': tech_preet},
        {'name': 'Epson Projector', 'category': 'Office Equipment', 'location': 'Conference Room A', 'department': 'Admin', 'owner_name': 'Admin Team', 'status': 'operational', 'manufacturer': 'Epson', 'model': 'EB-2265U', 'default_team': 'IT Support Team', 'default_tech': tech_tirth},
        {'name': 'Canon Document Scanner', 'category': 'Office Equipment', 'location': 'Records Room', 'department': 'HR', 'owner_name': 'HR Team', 'status': 'maintenance', 'manufacturer': 'Canon', 'model': 'DR-C225', 'default_team': 'IT Support Team', 'default_tech': tech_preet},
        
        # Safety - Assigned to Facilities Team
        {'name': 'Fire Suppression System', 'category': 'Safety Equipment', 'location': 'Server Room', 'department': 'Facilities', 'owner_name': 'Facilities Team', 'status': 'operational', 'manufacturer': 'Kidde', 'model': 'FM-200', 'default_team': 'Facilities Team', 'default_tech': None},
        {'name': 'Emergency Generator', 'category': 'Safety Equipment', 'location': 'Basement', 'department': 'Facilities', 'owner_name': 'Facilities Team', 'status': 'operational', 'manufacturer': 'Cummins', 'model': 'C150D6', 'default_team': 'Facilities Team', 'default_tech': None},
    ]
    
    equipment_list = []
    for idx, data in enumerate(equipment_data, 1):
        cat_name = data.pop('category')
        team_name = data.pop('default_team', None)
        tech_user = data.pop('default_tech', None)
        
        eq = Equipment(
            code=f'EQ-{idx:04d}',
            category_id=categories[cat_name].id,
            default_team_id=teams[team_name].id if team_name else None,
            default_technician_id=tech_user.id if tech_user else None,
            purchase_date=datetime.now().date() - timedelta(days=random.randint(100, 1000)),
            warranty_expiry=datetime.now().date() + timedelta(days=random.randint(-100, 500)),
            cost=random.randint(10000, 500000),
            **data
        )
        db.session.add(eq)
        equipment_list.append(eq)
    db.session.commit()
    
    # ==================== MAINTENANCE REQUESTS ====================
    print("  Creating maintenance requests...")
    requests_data = [
        # New requests
        {'name': 'Laptop screen flickering', 'equipment_idx': 0, 'team': 'IT Support Team', 'stage': 'New', 'priority': 'normal', 'type': 'corrective', 'requester': 'John Doe'},
        {'name': 'Quarterly server maintenance', 'equipment_idx': 3, 'team': 'IT Support Team', 'stage': 'New', 'priority': 'low', 'type': 'preventive', 'requester': 'IT Admin'},
        {'name': 'Printer paper jam issue', 'equipment_idx': 12, 'team': 'IT Support Team', 'stage': 'New', 'priority': 'normal', 'type': 'corrective', 'requester': 'Reception'},
        
        # In Progress
        {'name': 'MacBook battery replacement', 'equipment_idx': 2, 'team': 'IT Support Team', 'stage': 'In Progress', 'priority': 'high', 'type': 'corrective', 'requester': 'Mike Wilson'},
        {'name': 'Forklift hydraulic repair', 'equipment_idx': 6, 'team': 'Mechanical Team', 'stage': 'In Progress', 'priority': 'urgent', 'type': 'corrective', 'requester': 'Warehouse Manager'},
        {'name': 'CNC machine calibration', 'equipment_idx': 7, 'team': 'Mechanical Team', 'stage': 'In Progress', 'priority': 'high', 'type': 'preventive', 'requester': 'Production Lead'},
        
        # Waiting Parts
        {'name': 'Robot arm motor replacement', 'equipment_idx': 9, 'team': 'Mechanical Team', 'stage': 'Waiting Parts', 'priority': 'urgent', 'type': 'corrective', 'requester': 'Production Manager'},
        {'name': 'Scanner roller replacement', 'equipment_idx': 14, 'team': 'IT Support Team', 'stage': 'Waiting Parts', 'priority': 'normal', 'type': 'corrective', 'requester': 'HR Manager'},
        
        # Under Review
        {'name': 'AC compressor repair', 'equipment_idx': 10, 'team': 'Facilities Team', 'stage': 'Under Review', 'priority': 'high', 'type': 'corrective', 'requester': 'Facilities Manager'},
        {'name': 'Generator annual service', 'equipment_idx': 16, 'team': 'Facilities Team', 'stage': 'Under Review', 'priority': 'normal', 'type': 'preventive', 'requester': 'Safety Officer'},
        
        # Completed
        {'name': 'Vehicle oil change', 'equipment_idx': 4, 'team': 'Mechanical Team', 'stage': 'Completed', 'priority': 'low', 'type': 'preventive', 'requester': 'Admin'},
        {'name': 'Projector lamp replacement', 'equipment_idx': 13, 'team': 'IT Support Team', 'stage': 'Completed', 'priority': 'normal', 'type': 'corrective', 'requester': 'Admin'},
        {'name': 'Fire system inspection', 'equipment_idx': 15, 'team': 'Facilities Team', 'stage': 'Completed', 'priority': 'high', 'type': 'preventive', 'requester': 'Safety Officer'},
    ]
    
    for idx, data in enumerate(requests_data, 1):
        req = MaintenanceRequest(
            reference=f'MR-{idx:05d}',
            name=data['name'],
            description=f"Maintenance request for {data['name']}. Reported by {data['requester']}.",
            equipment_id=equipment_list[data['equipment_idx']].id,
            team_id=teams[data['team']].id,
            stage_id=stages[data['stage']].id,
            priority=data['priority'],
            request_type=data['type'],
            requester_name=data['requester'],
            requester_email=f"{data['requester'].lower().replace(' ', '.')}@company.com",
            request_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            scheduled_date=datetime.utcnow() + timedelta(days=random.randint(-5, 15)),
            deadline=datetime.utcnow() + timedelta(days=random.randint(1, 20)),
            completed_date=datetime.utcnow() - timedelta(days=random.randint(1, 5)) if data['stage'] == 'Completed' else None
        )
        db.session.add(req)
    
    db.session.commit()
    
    print("✅ Database seeded successfully!")
    print(f"   - {User.query.count()} users")
    print(f"   - {MaintenanceStage.query.count()} stages")
    print(f"   - {EquipmentCategory.query.count()} categories")
    print(f"   - {MaintenanceTeam.query.count()} teams")
    print(f"   - {Equipment.query.count()} equipment items")
    print(f"   - {MaintenanceRequest.query.count()} maintenance requests")
    print("\n📧 Default Login Credentials:")
    print("   Admin: admin@gearguard.com / admin123")
    print("   Manager: abhi.gabani@gearguard.com / password123")
    print("   User: user@gearguard.com / user123")


if __name__ == '__main__':
    seed_database()
