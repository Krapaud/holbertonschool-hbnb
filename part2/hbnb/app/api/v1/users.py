from app.services import facade
from flask_restx import Namespace, Resource, fields
from app.models.user import UserModel

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        try:
            # Check for email uniqueness first
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Try to create the user (this will trigger validation)
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name,
                    'last_name': new_user.last_name, 'email': new_user.email}, 201

        except ValueError as e:
            # Handle validation errors from the model
            return {'message': str(e)}, 400
        except Exception as e:
            # Handle any other unexpected errors
            return {'error': 'Internal server error', 'message': str(e)}, 500


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        try:
            user_data = api.payload
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user:
                    return {'error': 'Email already registered'}, 400

            updated_user = facade.update_user(user_id, user_data)
            return {'id': updated_user.id, 'first_name': updated_user.first_name,
                        'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500
