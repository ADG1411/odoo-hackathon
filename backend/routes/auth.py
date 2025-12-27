# -*- coding: utf-8 -*-
"""
Authentication Routes
"""
from flask import Blueprint, jsonify, request, session
from functools import wraps
from datetime import datetime
from backend.models import db
from backend.models.user import User, Role, ActivityLog

auth = Blueprint('auth', __name__, url_prefix='/auth')


# ==================== DECORATORS ====================
def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user = User.query.get(session['user_id'])
            if not user or not user.role:
                return jsonify({'error': 'Access denied'}), 403
            
            if user.role.name not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def permission_required(permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user = User.query.get(session['user_id'])
            if not user or not user.has_permission(permission):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """Get current logged in user"""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])


def log_activity(action, entity_type=None, entity_id=None, description=None):
    """Log user activity"""
    user = get_current_user()
    log = ActivityLog(
        user_id=user.id if user else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string[:500] if request.user_agent else None
    )
    db.session.add(log)
    db.session.commit()


# ==================== AUTH ROUTES ====================
@auth.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    
    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First name and last name are required'}), 400
    
    # Check if email exists
    if User.query.filter_by(email=data['email'].lower()).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Get default role (User)
    default_role = Role.query.filter_by(name='User').first()
    
    # Create user
    user = User(
        email=data['email'].lower(),
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        role_id=default_role.id if default_role else None,
        is_active=True
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    log_activity('register', 'user', user.id, f'User {user.email} registered')
    
    return jsonify({
        'message': 'Registration successful',
        'user': user.to_dict()
    }), 201


@auth.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email'].lower()).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401
    
    # Set session
    session['user_id'] = user.id
    session['user_role'] = user.role.name if user.role else None
    session.permanent = True
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    log_activity('login', 'user', user.id, f'User {user.email} logged in')
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    })


@auth.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    user = get_current_user()
    if user:
        log_activity('logout', 'user', user.id, f'User {user.email} logged out')
    
    session.clear()
    return jsonify({'message': 'Logged out successfully'})


@auth.route('/me')
@login_required
def get_me():
    """Get current user profile"""
    user = get_current_user()
    return jsonify(user.to_dict())


@auth.route('/me', methods=['PUT'])
@login_required
def update_me():
    """Update current user profile"""
    user = get_current_user()
    data = request.json
    
    # Update allowed fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'phone' in data:
        user.phone = data['phone']
    
    db.session.commit()
    
    log_activity('update', 'user', user.id, 'Profile updated')
    
    return jsonify(user.to_dict())


@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    user = get_current_user()
    data = request.json
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current and new passwords are required'}), 400
    
    if not user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    log_activity('update', 'user', user.id, 'Password changed')
    
    return jsonify({'message': 'Password changed successfully'})


# ==================== USER MANAGEMENT (Admin only) ====================
@auth.route('/users')
@login_required
@permission_required('can_manage_users')
def get_users():
    """Get all users"""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users])


@auth.route('/users/<int:id>')
@login_required
@permission_required('can_manage_users')
def get_user(id):
    """Get specific user"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


@auth.route('/users', methods=['POST'])
@login_required
@permission_required('can_manage_users')
def create_user():
    """Create new user (admin)"""
    data = request.json
    
    if User.query.filter_by(email=data['email'].lower()).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        email=data['email'].lower(),
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        role_id=data.get('role_id'),
        team_id=data.get('team_id'),
        is_active=data.get('is_active', True)
    )
    user.set_password(data.get('password', 'changeme123'))
    
    db.session.add(user)
    db.session.commit()
    
    log_activity('create', 'user', user.id, f'Admin created user {user.email}')
    
    return jsonify(user.to_dict()), 201


@auth.route('/users/<int:id>', methods=['PUT'])
@login_required
@permission_required('can_manage_users')
def update_user(id):
    """Update user (admin)"""
    user = User.query.get_or_404(id)
    data = request.json
    
    for field in ['first_name', 'last_name', 'phone', 'role_id', 'team_id', 'is_active']:
        if field in data:
            setattr(user, field, data[field])
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    db.session.commit()
    
    log_activity('update', 'user', user.id, f'Admin updated user {user.email}')
    
    return jsonify(user.to_dict())


@auth.route('/users/<int:id>', methods=['DELETE'])
@login_required
@permission_required('can_manage_users')
def delete_user(id):
    """Delete user (admin)"""
    user = User.query.get_or_404(id)
    
    # Prevent self-deletion
    if user.id == session.get('user_id'):
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    log_activity('delete', 'user', id, f'Admin deleted user {email}')
    
    return '', 204


# ==================== ROLES ====================
@auth.route('/roles')
@login_required
def get_roles():
    """Get all roles"""
    roles = Role.query.all()
    return jsonify([r.to_dict() for r in roles])


# ==================== ACTIVITY LOGS ====================
@auth.route('/activity-logs')
@login_required
@permission_required('can_manage_users')
def get_activity_logs():
    """Get activity logs"""
    limit = request.args.get('limit', 100, type=int)
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    return jsonify([l.to_dict() for l in logs])
