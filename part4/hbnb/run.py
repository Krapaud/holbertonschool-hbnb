#!/usr/bin/env python3
"""Application entry point.

This module serves as the main entry point for the HBnB Evolution application.
It creates and runs the Flask application instance.
"""
from app import create_app

# Create the Flask application instance using the factory pattern
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode for development
    # Debug mode provides detailed error messages and auto-reloading
    app.run(debug=True)
