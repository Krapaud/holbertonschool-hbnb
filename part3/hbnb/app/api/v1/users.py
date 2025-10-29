from app.models.user import User
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user (Admin only)'),
    'password': fields.String(description='Password of the user (Admin only)')
})

@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        try:
            users = facade.get_all_users()
            return [{'id': user.id, 'first_name': user.first_name,
                     'last_name': user.last_name, 'email': user.email}
                    for user in users], 200
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new user (public) or create a user (admin only)"""
        user_data = api.payload
        
        # Check if a JWT token is present (optional authentication)
        is_admin = False
        is_authenticated = False
        try:
            verify_jwt_in_request(optional=True)
            claims = get_jwt()
            if claims:
                is_authenticated = True
                is_admin = claims.get('is_admin', False)
        except Exception:
            # No token or invalid token - proceed as public registration
            is_authenticated = False
            is_admin = False
        
        # If authenticated but not admin, deny access
        if is_authenticated and not is_admin:
            return {'error': 'Unauthorized action. Only admins can create users when authenticated.'}, 403
        
        try:
            # Check for email uniqueness first
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Validate password presence (flask-restx should already validate this)
            if 'password' not in user_data or not user_data['password']:
                return {'error': 'password is required'}, 400

            # Create user with password - it will be hashed in the model's __init__
            new_user = facade.create_user(user_data)
            
            # Return only user ID and success message
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201

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

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Forbidden - can only update own profile or admin privileges required')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        try:
            user_data = api.payload
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            # Allow admins to modify any user, regular users only themselves
            if not is_admin and current_user_id != user_id:
                return {'error': 'Unauthorized action.'}, 403

            # For regular users, prevent modifying email or password
            if not is_admin and ('email' in user_data or 'password' in user_data):
                return {'error': 'You cannot modify email or password.'}, 400

            # For admins, allow all fields but validate email uniqueness
            if is_admin and 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email is already in use'}, 400
            
            allowed_fields = ['first_name', 'last_name']
            if is_admin:
                allowed_fields.extend(['email', 'password'])
                
            filtered_data = {k: v for k, v in user_data.items() if k in allowed_fields}
            
            # Handle password hashing for admins
            if is_admin and 'password' in filtered_data:
                user = facade.get_user(user_id)
                if user:
                    user.hash_password(filtered_data['password'])
                    filtered_data['password'] = user.password  # Use the hashed password
                    
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            updated_user = facade.update_user(user_id, filtered_data)
            return {'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error',
                    'message': str(e)}, 500
