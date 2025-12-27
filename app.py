# -*- coding: utf-8 -*-
"""
GearGuard - The Ultimate Maintenance Tracker
Main Application Entry Point
"""
from flask import Flask
from datetime import timedelta
from backend.config import config
from backend.models import db
from backend.routes import api, views, auth


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__,
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(views)
    app.register_blueprint(auth)
    
    # Create tables and initialize roles
    with app.app_context():
        db.create_all()
        # Create default roles
        from backend.models.user import Role
        Role.create_default_roles()
    
    return app


# Create app instance
app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
