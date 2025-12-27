# -*- coding: utf-8 -*-
"""
GearGuard - View Routes
"""
from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@views.route('/login')
def login():
    """Login page"""
    return render_template('auth/login.html')


@views.route('/signup')
def signup():
    """Signup page"""
    return render_template('auth/signup.html')


@views.route('/equipment')
def equipment_list():
    """Equipment list page"""
    return render_template('equipment/list.html')


@views.route('/equipment/<int:id>')
def equipment_detail(id):
    """Equipment detail page"""
    return render_template('equipment/detail.html', equipment_id=id)


@views.route('/categories')
def categories():
    """Equipment categories page"""
    return render_template('equipment/categories.html')


@views.route('/teams')
def teams():
    """Teams management page"""
    return render_template('teams/list.html')


@views.route('/teams/<int:id>')
def team_detail(id):
    """Team detail page"""
    return render_template('teams/detail.html', team_id=id)


@views.route('/requests')
def requests_list():
    """Maintenance requests list view"""
    return render_template('requests/list.html')


@views.route('/requests/kanban')
def requests_kanban():
    """Maintenance requests kanban board"""
    return render_template('requests/kanban.html')


@views.route('/requests/<int:id>')
def request_detail(id):
    """Request detail page"""
    return render_template('requests/detail.html', request_id=id)


@views.route('/calendar')
def calendar():
    """Calendar view"""
    return render_template('calendar.html')


@views.route('/reports')
def reports():
    """Reports and analytics"""
    return render_template('reports.html')


@views.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')
