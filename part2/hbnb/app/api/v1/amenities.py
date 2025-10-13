from app.services import facade
from flask_restx import Namespace, Resource, fields

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the amenity response model
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(required=True, description='Unique identifier of the amenity'),
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the update response model
update_response_model = api.model('UpdateResponse', {
    'message': fields.String(required=True, description='Success message')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.marshal_with(amenity_response_model, code=201)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        try:
            # Validate required field
            if not amenity_data or 'name' not in amenity_data:
                return {'error': 'Name is required'}, 400

            # Validate name format
            name = amenity_data['name'].strip()
            if not name:
                return {'error': 'Name cannot be empty'}, 400

            # Try to create the amenity (this will trigger validation)
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201

        except ValueError as e:
            # Handle validation errors from the model
            return {'error': str(e)}, 400
        except Exception as e:
            # Handle any other unexpected errors
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.marshal_list_with(amenity_response_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [{'id': amenity.id, 'name': amenity.name}
                    for amenity in amenities], 200
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_response_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.expect(amenity_model)
    @api.marshal_with(update_response_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            # Check if amenity exists
            existing_amenity = facade.get_amenity(amenity_id)
            if not existing_amenity:
                return {'error': 'Amenity not found'}, 404

            amenity_data = api.payload

            # Validate required field
            if not amenity_data or 'name' not in amenity_data:
                return {'error': 'Name is required'}, 400

            # Validate name format
            name = amenity_data['name'].strip()
            if not name:
                return {'error': 'Name cannot be empty'}, 400

            # Update the amenity
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {'message': 'Amenity updated successfully'}, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500
