from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.users import api as users_ns
from flask import Flask, jsonify
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1:places')

    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Add a simple root route
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Welcome to HBnB API',
            'documentation': '/api/v1/',
            'endpoints': {
                'users': '/api/v1/users',
                'places': '/api/v1/places',
                'amenities': '/api/v1/amenities',
                'reviews': '/api/v1/reviews'
            }
        })
    return app
