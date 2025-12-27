# -*- coding: utf-8 -*-
"""
GearGuard - API Routes with Authentication
"""
from flask import Blueprint, jsonify, request, session
from backend.models import db, EquipmentCategory, Equipment, MaintenanceTeam, TeamMember, MaintenanceStage, MaintenanceRequest
from backend.routes.auth import login_required, permission_required, get_current_user, log_activity
from datetime import datetime, timedelta
from sqlalchemy import func

api = Blueprint('api', __name__, url_prefix='/api')


# ==================== DASHBOARD ====================
@api.route('/dashboard/stats')
def dashboard_stats():
    """Get dashboard statistics"""
    total_equipment = Equipment.query.count()
    operational = Equipment.query.filter_by(status='operational').count()
    in_maintenance = Equipment.query.filter_by(status='maintenance').count()
    broken = Equipment.query.filter_by(status='broken').count()
    
    total_requests = MaintenanceRequest.query.count()
    
    # Open requests (not done, not scrapped)
    open_requests = db.session.query(MaintenanceRequest).join(MaintenanceStage).filter(
        MaintenanceStage.is_done == False,
        MaintenanceStage.is_scrap == False
    ).count()
    
    # Overdue requests
    overdue = db.session.query(MaintenanceRequest).join(MaintenanceStage).filter(
        MaintenanceStage.is_done == False,
        MaintenanceStage.is_scrap == False,
        MaintenanceRequest.deadline < datetime.utcnow()
    ).count()
    
    teams = MaintenanceTeam.query.filter_by(is_active=True).count()
    
    # Completed this month
    first_day = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    completed_this_month = db.session.query(MaintenanceRequest).join(MaintenanceStage).filter(
        MaintenanceStage.is_done == True,
        MaintenanceRequest.completed_date >= first_day
    ).count()
    
    return jsonify({
        'equipment': {
            'total': total_equipment,
            'operational': operational,
            'maintenance': in_maintenance,
            'broken': broken
        },
        'requests': {
            'total': total_requests,
            'open': open_requests,
            'overdue': overdue,
            'completed_this_month': completed_this_month
        },
        'teams': teams
    })


@api.route('/dashboard/recent-requests')
def recent_requests():
    """Get recent maintenance requests"""
    requests_list = MaintenanceRequest.query.order_by(
        MaintenanceRequest.created_at.desc()
    ).limit(10).all()
    return jsonify([r.to_dict() for r in requests_list])


@api.route('/dashboard/requests-by-stage')
def requests_by_stage():
    """Get request counts by stage for chart"""
    stages = MaintenanceStage.query.order_by(MaintenanceStage.sequence).all()
    return jsonify([{
        'name': s.name,
        'count': s.request_count,
        'color': s.color
    } for s in stages])


@api.route('/dashboard/requests-by-priority')
def requests_by_priority():
    """Get request counts by priority"""
    priorities = ['low', 'normal', 'high', 'urgent']
    result = []
    for p in priorities:
        count = MaintenanceRequest.query.filter_by(priority=p).count()
        result.append({'priority': p, 'count': count})
    return jsonify(result)


@api.route('/dashboard/equipment-by-status')
def equipment_by_status():
    """Get equipment counts by status"""
    statuses = ['operational', 'maintenance', 'broken', 'scrapped']
    colors = {'operational': '#28a745', 'maintenance': '#ffc107', 'broken': '#dc3545', 'scrapped': '#6c757d'}
    result = []
    for s in statuses:
        count = Equipment.query.filter_by(status=s).count()
        result.append({'status': s, 'count': count, 'color': colors[s]})
    return jsonify(result)


@api.route('/dashboard/monthly-requests')
def monthly_requests():
    """Get request counts for last 6 months"""
    result = []
    for i in range(5, -1, -1):
        date = datetime.utcnow() - timedelta(days=i*30)
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if date.month == 12:
            month_end = month_start.replace(year=date.year+1, month=1)
        else:
            month_end = month_start.replace(month=date.month+1)
        
        count = MaintenanceRequest.query.filter(
            MaintenanceRequest.created_at >= month_start,
            MaintenanceRequest.created_at < month_end
        ).count()
        
        result.append({
            'month': month_start.strftime('%b %Y'),
            'count': count
        })
    return jsonify(result)


# ==================== EQUIPMENT CATEGORIES ====================
@api.route('/categories')
def get_categories():
    """Get all equipment categories"""
    categories = EquipmentCategory.query.order_by(EquipmentCategory.name).all()
    return jsonify([c.to_dict() for c in categories])


@api.route('/categories/<int:id>')
def get_category(id):
    """Get single category"""
    category = EquipmentCategory.query.get_or_404(id)
    return jsonify(category.to_dict())


@api.route('/categories', methods=['POST'])
@login_required
@permission_required('can_manage_equipment')
def create_category():
    """Create new category"""
    data = request.json
    category = EquipmentCategory(
        name=data['name'],
        description=data.get('description'),
        color=data.get('color', '#6c757d'),
        icon=data.get('icon', 'bi-box')
    )
    db.session.add(category)
    db.session.commit()
    
    log_activity('create', 'category', category.id, f'Created category: {category.name}')
    return jsonify(category.to_dict()), 201


@api.route('/categories/<int:id>', methods=['PUT'])
@login_required
@permission_required('can_manage_equipment')
def update_category(id):
    """Update category"""
    category = EquipmentCategory.query.get_or_404(id)
    data = request.json
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    category.color = data.get('color', category.color)
    category.icon = data.get('icon', category.icon)
    db.session.commit()
    
    log_activity('update', 'category', category.id, f'Updated category: {category.name}')
    return jsonify(category.to_dict())


@api.route('/categories/<int:id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_equipment')
def delete_category(id):
    """Delete category"""
    category = EquipmentCategory.query.get_or_404(id)
    name = category.name
    db.session.delete(category)
    db.session.commit()
    
    log_activity('delete', 'category', id, f'Deleted category: {name}')
    return '', 204


# ==================== EQUIPMENT ====================
@api.route('/equipment')
def get_equipment():
    """Get all equipment with optional filters"""
    query = Equipment.query
    
    # Filters
    status = request.args.get('status')
    category_id = request.args.get('category_id')
    department = request.args.get('department')
    search = request.args.get('search')
    
    if status:
        query = query.filter_by(status=status)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if department:
        query = query.filter_by(department=department)
    if search:
        query = query.filter(
            db.or_(
                Equipment.name.ilike(f'%{search}%'),
                Equipment.code.ilike(f'%{search}%'),
                Equipment.serial_number.ilike(f'%{search}%')
            )
        )
    
    equipment_list = query.order_by(Equipment.code).all()
    return jsonify([e.to_dict() for e in equipment_list])


@api.route('/equipment/<int:id>')
def get_equipment_by_id(id):
    """Get single equipment with full details"""
    equipment = Equipment.query.get_or_404(id)
    data = equipment.to_dict()
    
    # Add maintenance history
    data['maintenance_history'] = [r.to_dict() for r in 
        equipment.maintenance_requests.order_by(MaintenanceRequest.created_at.desc()).limit(10).all()]
    
    return jsonify(data)


@api.route('/equipment', methods=['POST'])
@login_required
@permission_required('can_manage_equipment')
def create_equipment():
    """Create new equipment"""
    data = request.json
    equipment = Equipment(
        code=Equipment.generate_code(),
        name=data['name'],
        category_id=data.get('category_id'),
        serial_number=data.get('serial_number'),
        model=data.get('model'),
        manufacturer=data.get('manufacturer'),
        location=data.get('location'),
        department=data.get('department'),
        owner_name=data.get('owner_name'),
        owner_email=data.get('owner_email'),
        default_team_id=data.get('default_team_id'),
        default_technician_id=data.get('default_technician_id'),
        status=data.get('status', 'operational'),
        purchase_date=datetime.fromisoformat(data['purchase_date']).date() if data.get('purchase_date') else None,
        warranty_expiry=datetime.fromisoformat(data['warranty_expiry']).date() if data.get('warranty_expiry') else None,
        cost=data.get('cost'),
        notes=data.get('notes')
    )
    db.session.add(equipment)
    db.session.commit()
    
    log_activity('create', 'equipment', equipment.id, f'Created equipment: {equipment.code} - {equipment.name}')
    return jsonify(equipment.to_dict()), 201


@api.route('/equipment/<int:id>', methods=['PUT'])
@login_required
@permission_required('can_manage_equipment')
def update_equipment(id):
    """Update equipment"""
    equipment = Equipment.query.get_or_404(id)
    data = request.json
    
    for field in ['name', 'category_id', 'serial_number', 'model', 'manufacturer',
                  'location', 'department', 'owner_name', 'owner_email', 
                  'default_team_id', 'default_technician_id', 'status', 'cost', 'notes']:
        if field in data:
            setattr(equipment, field, data[field])
    
    if 'purchase_date' in data:
        equipment.purchase_date = datetime.fromisoformat(data['purchase_date']).date() if data['purchase_date'] else None
    if 'warranty_expiry' in data:
        equipment.warranty_expiry = datetime.fromisoformat(data['warranty_expiry']).date() if data['warranty_expiry'] else None
    
    db.session.commit()
    
    log_activity('update', 'equipment', equipment.id, f'Updated equipment: {equipment.code}')
    return jsonify(equipment.to_dict())


@api.route('/equipment/<int:id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_equipment')
def delete_equipment(id):
    """Delete equipment"""
    equipment = Equipment.query.get_or_404(id)
    code = equipment.code
    db.session.delete(equipment)
    db.session.commit()
    
    log_activity('delete', 'equipment', id, f'Deleted equipment: {code}')
    return '', 204


@api.route('/equipment/departments')
def get_departments():
    """Get unique departments"""
    departments = db.session.query(Equipment.department).filter(
        Equipment.department.isnot(None)
    ).distinct().all()
    return jsonify([d[0] for d in departments if d[0]])


@api.route('/equipment/<int:id>/autofill')
def equipment_autofill(id):
    """Get auto-fill data when equipment is selected (for request forms)
    
    Returns category, default team, and default technician for auto-filling request forms.
    This implements the Flow 1 requirement: When user selects Equipment, system 
    auto-fills the Equipment category and Maintenance Team.
    """
    equipment = Equipment.query.get_or_404(id)
    
    return jsonify({
        'equipment_id': equipment.id,
        'equipment_name': equipment.name,
        'equipment_code': equipment.code,
        'category_id': equipment.category_id,
        'category_name': equipment.category.name if equipment.category else None,
        'default_team_id': equipment.default_team_id,
        'default_team_name': equipment.default_team.name if equipment.default_team else None,
        'default_technician_id': equipment.default_technician_id,
        'default_technician_name': equipment.default_technician.full_name if equipment.default_technician else None,
        'location': equipment.location,
        'department': equipment.department,
        'owner_name': equipment.owner_name,
        'owner_email': equipment.owner_email
    })


@api.route('/equipment/<int:id>/scrap', methods=['POST'])
@login_required
@permission_required('can_manage_equipment')
def scrap_equipment(id):
    """Mark equipment as scrapped with reason/notes
    
    This implements the Scrap Logic requirement:
    - Update Equipment status to Scrapped
    - Record scrap date and reason
    - Log the activity
    """
    equipment = Equipment.query.get_or_404(id)
    data = request.json
    
    equipment.status = 'scrapped'
    equipment.is_scrapped = True
    equipment.scrap_date = datetime.utcnow().date()
    equipment.scrap_reason = data.get('reason', 'No reason provided')
    
    db.session.commit()
    
    log_activity('scrap', 'equipment', equipment.id, 
                 f'Scrapped equipment: {equipment.code} - Reason: {equipment.scrap_reason}')
    
    return jsonify(equipment.to_dict())


@api.route('/equipment/<int:id>/requests')
def equipment_requests(id):
    """Get all maintenance requests for specific equipment (Smart Button)
    
    This implements the Smart Button requirement showing all maintenance
    requests related to a specific piece of equipment.
    """
    equipment = Equipment.query.get_or_404(id)
    
    requests_list = equipment.maintenance_requests.order_by(
        MaintenanceRequest.created_at.desc()
    ).all()
    
    return jsonify({
        'equipment_id': equipment.id,
        'equipment_code': equipment.code,
        'equipment_name': equipment.name,
        'total_requests': len(requests_list),
        'open_requests': equipment.open_request_count,
        'requests': [r.to_dict() for r in requests_list]
    })


# ==================== MAINTENANCE TEAMS ====================
@api.route('/teams')
def get_teams():
    """Get all teams"""
    teams = MaintenanceTeam.query.order_by(MaintenanceTeam.name).all()
    return jsonify([t.to_dict() for t in teams])


@api.route('/teams/<int:id>')
def get_team(id):
    """Get single team with members"""
    team = MaintenanceTeam.query.get_or_404(id)
    data = team.to_dict()
    
    # Add open requests count
    data['open_requests'] = db.session.query(MaintenanceRequest).join(MaintenanceStage).filter(
        MaintenanceRequest.team_id == id,
        MaintenanceStage.is_done == False,
        MaintenanceStage.is_scrap == False
    ).count()
    
    return jsonify(data)


@api.route('/teams', methods=['POST'])
@login_required
@permission_required('can_manage_teams')
def create_team():
    """Create new team"""
    data = request.json
    team = MaintenanceTeam(
        name=data['name'],
        description=data.get('description'),
        color=data.get('color', '#0d6efd'),
        leader_name=data.get('leader_name'),
        leader_email=data.get('leader_email'),
        leader_phone=data.get('leader_phone')
    )
    db.session.add(team)
    db.session.commit()
    
    log_activity('create', 'team', team.id, f'Created team: {team.name}')
    return jsonify(team.to_dict()), 201


@api.route('/teams/<int:id>', methods=['PUT'])
@login_required
@permission_required('can_manage_teams')
def update_team(id):
    """Update team"""
    team = MaintenanceTeam.query.get_or_404(id)
    data = request.json
    
    for field in ['name', 'description', 'color', 'leader_name', 'leader_email', 'leader_phone', 'is_active']:
        if field in data:
            setattr(team, field, data[field])
    
    db.session.commit()
    
    log_activity('update', 'team', team.id, f'Updated team: {team.name}')
    return jsonify(team.to_dict())


@api.route('/teams/<int:id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_teams')
def delete_team(id):
    """Delete team"""
    team = MaintenanceTeam.query.get_or_404(id)
    name = team.name
    db.session.delete(team)
    db.session.commit()
    
    log_activity('delete', 'team', id, f'Deleted team: {name}')
    return '', 204


@api.route('/teams/<int:team_id>/members', methods=['POST'])
@login_required
@permission_required('can_manage_teams')
def add_team_member(team_id):
    """Add member to team"""
    team = MaintenanceTeam.query.get_or_404(team_id)
    data = request.json
    member = TeamMember(
        team_id=team_id,
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        role=data.get('role', 'Technician')
    )
    db.session.add(member)
    db.session.commit()
    
    log_activity('create', 'team_member', member.id, f'Added member {member.name} to team {team.name}')
    return jsonify(member.to_dict()), 201


@api.route('/teams/<int:team_id>/members/<int:member_id>', methods=['PUT'])
@login_required
@permission_required('can_manage_teams')
def update_team_member(team_id, member_id):
    """Update team member"""
    member = TeamMember.query.filter_by(id=member_id, team_id=team_id).first_or_404()
    data = request.json
    
    for field in ['name', 'email', 'phone', 'role', 'is_active']:
        if field in data:
            setattr(member, field, data[field])
    
    db.session.commit()
    return jsonify(member.to_dict())


@api.route('/teams/<int:team_id>/members/<int:member_id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_teams')
def remove_team_member(team_id, member_id):
    """Remove member from team"""
    member = TeamMember.query.filter_by(id=member_id, team_id=team_id).first_or_404()
    db.session.delete(member)
    db.session.commit()
    
    log_activity('delete', 'team_member', member_id, f'Removed member from team')
    return '', 204


# ==================== MAINTENANCE STAGES ====================
@api.route('/stages')
def get_stages():
    """Get all stages"""
    stages = MaintenanceStage.query.order_by(MaintenanceStage.sequence).all()
    return jsonify([s.to_dict() for s in stages])


@api.route('/stages', methods=['POST'])
@login_required
@permission_required('can_manage_settings')
def create_stage():
    """Create new stage"""
    data = request.json
    stage = MaintenanceStage(
        name=data['name'],
        sequence=data.get('sequence', 10),
        color=data.get('color', '#6c757d'),
        is_done=data.get('is_done', False),
        is_scrap=data.get('is_scrap', False),
        fold=data.get('fold', False)
    )
    db.session.add(stage)
    db.session.commit()
    
    log_activity('create', 'stage', stage.id, f'Created stage: {stage.name}')
    return jsonify(stage.to_dict()), 201


@api.route('/stages/<int:id>', methods=['PUT'])
@login_required
@permission_required('can_manage_settings')
def update_stage(id):
    """Update stage"""
    stage = MaintenanceStage.query.get_or_404(id)
    data = request.json
    
    for field in ['name', 'sequence', 'color', 'is_done', 'is_scrap', 'fold']:
        if field in data:
            setattr(stage, field, data[field])
    
    db.session.commit()
    
    log_activity('update', 'stage', stage.id, f'Updated stage: {stage.name}')
    return jsonify(stage.to_dict())


@api.route('/stages/<int:id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_settings')
def delete_stage(id):
    """Delete stage"""
    stage = MaintenanceStage.query.get_or_404(id)
    
    # Check if stage has requests
    if stage.requests.count() > 0:
        return jsonify({'error': 'Cannot delete stage with existing requests'}), 400
    
    name = stage.name
    db.session.delete(stage)
    db.session.commit()
    
    log_activity('delete', 'stage', id, f'Deleted stage: {name}')
    return '', 204


# ==================== MAINTENANCE REQUESTS ====================
@api.route('/requests')
def get_requests():
    """Get all requests with optional filters"""
    query = MaintenanceRequest.query
    
    # Filters
    stage_id = request.args.get('stage_id')
    team_id = request.args.get('team_id')
    equipment_id = request.args.get('equipment_id')
    priority = request.args.get('priority')
    request_type = request.args.get('request_type')
    search = request.args.get('search')
    overdue_only = request.args.get('overdue') == 'true'
    
    if stage_id:
        query = query.filter_by(stage_id=stage_id)
    if team_id:
        query = query.filter_by(team_id=team_id)
    if equipment_id:
        query = query.filter_by(equipment_id=equipment_id)
    if priority:
        query = query.filter_by(priority=priority)
    if request_type:
        query = query.filter_by(request_type=request_type)
    if search:
        query = query.filter(
            db.or_(
                MaintenanceRequest.name.ilike(f'%{search}%'),
                MaintenanceRequest.reference.ilike(f'%{search}%'),
                MaintenanceRequest.description.ilike(f'%{search}%')
            )
        )
    if overdue_only:
        query = query.join(MaintenanceStage).filter(
            MaintenanceStage.is_done == False,
            MaintenanceStage.is_scrap == False,
            MaintenanceRequest.deadline < datetime.utcnow()
        )
    
    requests_list = query.order_by(MaintenanceRequest.created_at.desc()).all()
    return jsonify([r.to_dict() for r in requests_list])


@api.route('/requests/<int:id>')
def get_request(id):
    """Get single request"""
    req = MaintenanceRequest.query.get_or_404(id)
    return jsonify(req.to_dict())


@api.route('/requests', methods=['POST'])
@login_required
def create_request():
    """Create new maintenance request"""
    data = request.json
    user = get_current_user()
    
    # Get first stage as default
    default_stage = MaintenanceStage.query.order_by(MaintenanceStage.sequence).first()
    
    req = MaintenanceRequest(
        reference=MaintenanceRequest.generate_reference(),
        name=data['name'],
        description=data.get('description'),
        equipment_id=data.get('equipment_id'),
        team_id=data.get('team_id'),
        stage_id=data.get('stage_id') or (default_stage.id if default_stage else None),
        request_type=data.get('request_type', 'corrective'),
        priority=data.get('priority', 'normal'),
        requester_name=data.get('requester_name') or (user.full_name if user else None),
        requester_email=data.get('requester_email') or (user.email if user else None),
        requester_phone=data.get('requester_phone'),
        scheduled_date=datetime.fromisoformat(data['scheduled_date']) if data.get('scheduled_date') else None,
        deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None
    )
    db.session.add(req)
    db.session.commit()
    
    log_activity('create', 'request', req.id, f'Created request: {req.reference}')
    return jsonify(req.to_dict()), 201


@api.route('/requests/<int:id>', methods=['PUT'])
@login_required
def update_request(id):
    """Update request"""
    req = MaintenanceRequest.query.get_or_404(id)
    data = request.json
    user = get_current_user()
    
    # Check permissions
    if not user.has_permission('can_manage_requests'):
        # Regular users can only update their own requests
        if req.requester_email != user.email:
            return jsonify({'error': 'Permission denied'}), 403
    
    for field in ['name', 'description', 'equipment_id', 'team_id', 'stage_id',
                  'request_type', 'priority', 'requester_name', 'requester_email',
                  'requester_phone', 'duration_hours', 'maintenance_cost',
                  'technician_notes', 'resolution']:
        if field in data:
            setattr(req, field, data[field])
    
    if 'scheduled_date' in data:
        req.scheduled_date = datetime.fromisoformat(data['scheduled_date']) if data['scheduled_date'] else None
    if 'deadline' in data:
        req.deadline = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
    if 'completed_date' in data:
        req.completed_date = datetime.fromisoformat(data['completed_date']) if data['completed_date'] else None
    
    # If moved to done stage, set completed date
    if 'stage_id' in data:
        stage = MaintenanceStage.query.get(data['stage_id'])
        if stage and stage.is_done and not req.completed_date:
            req.completed_date = datetime.utcnow()
        # Update equipment status if scrapped
        if stage and stage.is_scrap and req.equipment:
            req.equipment.status = 'scrapped'
    
    db.session.commit()
    
    log_activity('update', 'request', req.id, f'Updated request: {req.reference}')
    return jsonify(req.to_dict())


@api.route('/requests/<int:id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_requests')
def delete_request(id):
    """Delete request"""
    req = MaintenanceRequest.query.get_or_404(id)
    reference = req.reference
    db.session.delete(req)
    db.session.commit()
    
    log_activity('delete', 'request', id, f'Deleted request: {reference}')
    return '', 204


@api.route('/requests/<int:id>/move-stage', methods=['POST'])
@login_required
def move_request_stage(id):
    """Move request to different stage (for kanban drag & drop)"""
    req = MaintenanceRequest.query.get_or_404(id)
    data = request.json
    new_stage_id = data.get('stage_id')
    user = get_current_user()
    
    if new_stage_id:
        stage = MaintenanceStage.query.get_or_404(new_stage_id)
        
        # Check if user can complete requests (for done/scrap stages)
        if (stage.is_done or stage.is_scrap) and not user.has_permission('can_complete_requests'):
            return jsonify({'error': 'Permission denied'}), 403
        
        old_stage_name = req.stage.name if req.stage else 'None'
        req.stage_id = new_stage_id
        
        # Auto-set completed date when moved to done stage
        if stage.is_done and not req.completed_date:
            req.completed_date = datetime.utcnow()
        
        # Update equipment status if scrapped
        if stage.is_scrap and req.equipment:
            req.equipment.status = 'scrapped'
        
        db.session.commit()
        
        log_activity('update', 'request', req.id, f'Moved {req.reference} from {old_stage_name} to {stage.name}')
    
    return jsonify(req.to_dict())


@api.route('/requests/<int:id>/assign', methods=['POST'])
@login_required
@permission_required('can_assign_requests')
def assign_request(id):
    """Assign request to team"""
    req = MaintenanceRequest.query.get_or_404(id)
    data = request.json
    
    req.team_id = data.get('team_id')
    db.session.commit()
    
    team_name = req.team.name if req.team else 'Unassigned'
    log_activity('update', 'request', req.id, f'Assigned {req.reference} to {team_name}')
    
    return jsonify(req.to_dict())


# ==================== CALENDAR ====================
@api.route('/calendar/events')
def calendar_events():
    """Get maintenance requests as calendar events"""
    start = request.args.get('start')
    end = request.args.get('end')
    
    query = MaintenanceRequest.query.filter(
        MaintenanceRequest.scheduled_date.isnot(None)
    )
    
    if start:
        query = query.filter(MaintenanceRequest.scheduled_date >= datetime.fromisoformat(start.replace('Z', '')))
    if end:
        query = query.filter(MaintenanceRequest.scheduled_date <= datetime.fromisoformat(end.replace('Z', '')))
    
    requests_list = query.all()
    
    events = []
    for req in requests_list:
        color = req.stage.color if req.stage else '#6c757d'
        events.append({
            'id': req.id,
            'title': f'{req.reference}: {req.name}',
            'start': req.scheduled_date.isoformat(),
            'end': req.scheduled_date.isoformat(),
            'color': color,
            'extendedProps': {
                'reference': req.reference,
                'equipment': req.equipment.name if req.equipment else None,
                'team': req.team.name if req.team else None,
                'priority': req.priority,
                'is_overdue': req.is_overdue
            }
        })
    
    return jsonify(events)


# ==================== REPORTS ====================
@api.route('/reports/summary')
@login_required
@permission_required('can_view_reports')
def reports_summary():
    """Get reports summary data"""
    # Requests by type
    corrective = MaintenanceRequest.query.filter_by(request_type='corrective').count()
    preventive = MaintenanceRequest.query.filter_by(request_type='preventive').count()
    
    # Average resolution time (for completed requests)
    completed = MaintenanceRequest.query.filter(
        MaintenanceRequest.completed_date.isnot(None),
        MaintenanceRequest.request_date.isnot(None)
    ).all()
    
    avg_resolution_hours = 0
    if completed:
        total_hours = sum([(r.completed_date - r.request_date).total_seconds() / 3600 for r in completed])
        avg_resolution_hours = round(total_hours / len(completed), 1)
    
    # Equipment utilization
    total_eq = Equipment.query.count()
    eq_with_requests = db.session.query(func.count(func.distinct(MaintenanceRequest.equipment_id))).scalar()
    
    # Team workload
    team_workload = []
    teams = MaintenanceTeam.query.all()
    for team in teams:
        open_count = db.session.query(MaintenanceRequest).join(MaintenanceStage).filter(
            MaintenanceRequest.team_id == team.id,
            MaintenanceStage.is_done == False,
            MaintenanceStage.is_scrap == False
        ).count()
        total_count = MaintenanceRequest.query.filter_by(team_id=team.id).count()
        team_workload.append({
            'team': team.name,
            'color': team.color,
            'open': open_count,
            'total': total_count
        })
    
    return jsonify({
        'requests_by_type': {
            'corrective': corrective,
            'preventive': preventive
        },
        'avg_resolution_hours': avg_resolution_hours,
        'equipment_utilization': {
            'total': total_eq,
            'with_requests': eq_with_requests
        },
        'team_workload': team_workload
    })


@api.route('/reports/equipment-breakdown')
@login_required
@permission_required('can_view_reports')
def equipment_breakdown_report():
    """Get equipment breakdown analysis"""
    # Equipment by category
    by_category = db.session.query(
        EquipmentCategory.name,
        func.count(Equipment.id)
    ).join(Equipment, Equipment.category_id == EquipmentCategory.id
    ).group_by(EquipmentCategory.name).all()
    
    # Equipment by status
    by_status = db.session.query(
        Equipment.status,
        func.count(Equipment.id)
    ).group_by(Equipment.status).all()
    
    # Equipment by department
    by_department = db.session.query(
        Equipment.department,
        func.count(Equipment.id)
    ).filter(Equipment.department.isnot(None)
    ).group_by(Equipment.department).all()
    
    # Most maintained equipment (top 10)
    most_maintained = db.session.query(
        Equipment.code,
        Equipment.name,
        func.count(MaintenanceRequest.id).label('request_count')
    ).join(MaintenanceRequest, MaintenanceRequest.equipment_id == Equipment.id
    ).group_by(Equipment.id
    ).order_by(func.count(MaintenanceRequest.id).desc()
    ).limit(10).all()
    
    return jsonify({
        'by_category': [{'name': c[0], 'count': c[1]} for c in by_category],
        'by_status': [{'status': s[0], 'count': s[1]} for s in by_status],
        'by_department': [{'department': d[0] or 'Unassigned', 'count': d[1]} for d in by_department],
        'most_maintained': [{'code': m[0], 'name': m[1], 'count': m[2]} for m in most_maintained]
    })


@api.route('/reports/maintenance-trends')
@login_required
@permission_required('can_view_reports')
def maintenance_trends_report():
    """Get maintenance trends over time"""
    result = []
    
    for i in range(11, -1, -1):  # Last 12 months
        date = datetime.utcnow() - timedelta(days=i*30)
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if date.month == 12:
            month_end = month_start.replace(year=date.year+1, month=1)
        else:
            month_end = month_start.replace(month=date.month+1)
        
        created = MaintenanceRequest.query.filter(
            MaintenanceRequest.created_at >= month_start,
            MaintenanceRequest.created_at < month_end
        ).count()
        
        completed = MaintenanceRequest.query.filter(
            MaintenanceRequest.completed_date >= month_start,
            MaintenanceRequest.completed_date < month_end
        ).count()
        
        result.append({
            'month': month_start.strftime('%b %Y'),
            'created': created,
            'completed': completed
        })
    
    return jsonify(result)


# ==================== USERS (for technician selection) ====================
@api.route('/users/technicians')
def get_technicians():
    """Get users who can be assigned as technicians"""
    from backend.models.user import User
    # Get users with technician or higher role
    users = User.query.filter(User.is_active == True).all()
    return jsonify([{
        'id': u.id,
        'name': u.full_name,
        'email': u.email,
        'role': u.role.name if u.role else None
    } for u in users])


@api.route('/users')
@login_required
@permission_required('can_manage_users')
def get_all_users():
    """Get all users (admin only)"""
    from backend.models.user import User
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
