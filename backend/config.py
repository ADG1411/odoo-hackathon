# -*- coding: utf-8 -*-
"""
GearGuard - Configuration Settings
"""
import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gearguard-secret-key-2024'
    
    # Database - Use SQLite for development, PostgreSQL for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///gearguard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # App Settings
    APP_NAME = 'GearGuard'
    APP_VERSION = '1.0.0'
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
