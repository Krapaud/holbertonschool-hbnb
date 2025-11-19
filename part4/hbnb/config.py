#!/usr/bin/env python3
"""Application configuration module.

This module defines configuration classes for different environments
(development, production, testing). Each configuration class contains
settings for database connections, secret keys, and Flask options.
"""
import os


class Config:
    """Base configuration class.
    
    Contains default settings that are common to all environments.
    Other configuration classes inherit from this base class.
    """
    # Secret key for session management and CSRF protection
    # In production, this should be set via environment variable
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # Debug mode disabled by default for security
    DEBUG = False


class DevelopmentConfig(Config):
    """Development environment configuration.
    
    Enables debug mode and uses SQLite database for local development.
    Inherits all settings from the base Config class.
    """
    # Enable debug mode for detailed error messages during development
    DEBUG = True
    
    # SQLite database URI for local development
    # Creates a file named 'development.db' in the instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    
    # Disable modification tracking to improve performance
    # Set to False to suppress deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuration dictionary mapping environment names to config classes
# Used by the application factory to select the appropriate configuration
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
