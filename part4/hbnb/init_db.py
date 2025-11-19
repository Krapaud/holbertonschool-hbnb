#!/usr/bin/env python3
"""Database initialization script.

This script creates all database tables defined in the application models.
It should be run once before starting the application for the first time,
or whenever new models are added to the application.

Usage:
    python init_db.py
"""
from app import create_app, db

if __name__ == '__main__':
    # Create application instance to access database configuration
    app = create_app()
    
    # Push application context to make app and db available
    # This is required for SQLAlchemy operations outside of request handlers
    with app.app_context():
        # Create all tables defined in models that inherit from db.Model
        # This reads the model definitions and generates corresponding SQL
        db.create_all()
        print('Database tables created successfully!')
