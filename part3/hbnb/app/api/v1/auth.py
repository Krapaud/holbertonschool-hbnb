from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, jwt_required, get_jwt
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Success', token_model)
    @api.response(400, 'Missing credentials')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        if not credentials or 'email' not in credentials or 'password' not in credentials:
            return {'error': 'Email and password are required.'}, 400

        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        return {
            'message': 'Login successful',
            'access_token': access_token
        }, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        
        # Récupération de l’identité de l’utilisateur (l’ID, passé en 'identity' au login)
        current_user = get_jwt_identity()
        
        # Récupération des claims additionnels (comme is_admin)
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        return {
            'message': f'Hello user {current_user}',
            'is_admin': is_admin
        }, 200
