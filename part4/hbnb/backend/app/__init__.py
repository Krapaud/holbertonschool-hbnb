#!/usr/bin/env python3
"""Application factory module.

This module defines the Flask application factory pattern.
It initializes all extensions (database, authentication, API)
and registers all routes and namespaces.
"""
from flask import Flask, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask extensions
# These are initialized here but configured in create_app()
bcrypt = Bcrypt()  # Password hashing
jwt = JWTManager()  # JWT token management
db = SQLAlchemy()  # Database ORM


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application.
    
    This function implements the application factory pattern,
    which allows creating multiple app instances with different configs.
    
    Args:
        config_class (str): Path to configuration class to use.
                           Default: "config.DevelopmentConfig"
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask application instance
    app = Flask(__name__, static_folder='../static')
    
    # Load configuration from the specified class
    app.config.from_object(config_class)
    
    # Configure CORS to allow requests from frontend
    # This must be done AFTER loading config
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=False)

    # Initialize extensions with the app instance
    bcrypt.init_app(app)  # Enable password hashing
    jwt.init_app(app)  # Enable JWT authentication
    db.init_app(app)  # Connect database ORM

    # Import API namespaces here to avoid circular imports
    # Each namespace handles a specific resource (users, places, etc.)
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns

    # Create Flask-RESTX API instance with documentation
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/')  # Swagger documentation available at /api/v1/

    # Register all API namespaces with their URL prefixes
    # This creates the RESTful API structure
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # ============================================
    # HTML PAGES ROUTES - REMOVED FOR FRONTEND/BACKEND SEPARATION
    # Frontend is now served separately (e.g., with python -m http.server)
    # This backend only serves the API endpoints
    # ============================================

    # ============================================
    # API INFO ROUTE
    # Provides information about available endpoints
    # ============================================
    
    @app.route('/api')
    @app.route('/api/')
    def api_info():
        """API information and available endpoints.
        
        Returns a JSON object with API documentation URL and
        list of available resource endpoints.
        
        Returns:
            dict: API information including endpoint URLs
        """
        return jsonify({
            'message': 'Welcome to HBnB API',
            'documentation': '/api/v1/',
            'endpoints': {
                'users': '/api/v1/users',
                'places': '/api/v1/places',
                'amenities': '/api/v1/amenities',
                'reviews': '/api/v1/reviews',
                'auth': '/api/v1/auth'
            }
        })
    
    return app
