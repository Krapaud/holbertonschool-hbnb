from flask import Flask, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Import namespaces here to avoid circular imports
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the auth namespace
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')

    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # ============================================
    # HTML PAGES ROUTES
    # Serve static HTML pages without /static/ in URL
    # ============================================
    
    @app.route('/')
    @app.route('/index.html')
    def index():
        """Serve the main index page"""
        return app.send_static_file('index.html')

    @app.route('/login.html')
    def login():
        """Serve the login page"""
        return app.send_static_file('login.html')

    @app.route('/place.html')
    def place():
        """Serve the place details page"""
        return app.send_static_file('place.html')

    @app.route('/add_review.html')
    def add_review():
        """Serve the add review page"""
        return app.send_static_file('add_review.html')

    # ============================================
    # API INFO ROUTE
    # ============================================
    
    @app.route('/api')
    @app.route('/api/')
    def api_info():
        """API information and available endpoints"""
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
