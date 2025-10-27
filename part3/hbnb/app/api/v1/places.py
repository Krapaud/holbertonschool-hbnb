from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=False,
                              description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Register a new place"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return {'error': 'Unauthorized action'}, 403
        place_data = api.payload
        place_data['owner_id'] = current_user_id
        # Validate input data types and required fields
        try:
            # Check for required fields
            required_fields = ['title', 'price', 'latitude', 'longitude']
            for field in required_fields:
                if field not in place_data:
                    return {'error': f'Missing required field: {field}'}, 400

            # Validate title is string and not empty
            if (not isinstance(place_data['title'], str) or
                    not place_data['title'].strip()):
                return {'error': 'Title must be a non-empty string'}, 400

            # Validate price is numeric (convert string to float if needed)
            if isinstance(place_data['price'], str):
                try:
                    place_data['price'] = float(place_data['price'])
                except ValueError:
                    return {'error': 'Price must be a valid number'}, 400
            elif not isinstance(place_data['price'], (int, float)):
                return {'error': 'Price must be a number'}, 400

            if place_data['price'] <= 0:
                return {'error': 'Price must be positive'}, 400

            # Validate latitude is numeric and in valid range
            if isinstance(place_data['latitude'], str):
                try:
                    place_data['latitude'] = float(place_data['latitude'])
                except ValueError:
                    return {'error': 'Latitude must be a valid number'}, 400
            elif not isinstance(place_data['latitude'], (int, float)):
                return {'error': 'Latitude must be a number'}, 400

            if not -90 <= place_data['latitude'] <= 90:
                return {'error': 'Latitude must be between -90 and 90'}, 400

            # Validate longitude is numeric and in valid range
            if isinstance(place_data['longitude'], str):
                try:
                    place_data['longitude'] = float(place_data['longitude'])
                except ValueError:
                    return {'error': 'Longitude must be a valid number'}, 400
            elif not isinstance(place_data['longitude'], (int, float)):
                return {'error': 'Longitude must be a number'}, 400

            if not -180 <= place_data['longitude'] <= 180:
                return {'error': 'Longitude must be between -180 and 180'}, 400

            existing_place = facade.get_place_by_title(place_data['title'])
            if existing_place:
                return {'error': 'Place already registered'}, 400
            new_place = facade.create_place(place_data)
            return {'id': new_place.id, 'title': new_place.title,
                    'price': new_place.price, 'latitude': new_place.latitude,
                    'longitude': new_place.longitude,
                    'owner_id': new_place.owner.id,
                    'description': new_place.description}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            place_dict = {
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude}
            result.append(place_dict)
        return result, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'description': place.description,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': amenity.id, 'name': amenity.name}
                          for amenity in place.amenities],
            'reviews': [{'id': review.id, 'text': review.text,
                         'rating': review.rating, 'user_id': review.user.id}
                        for review in place.reviews]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data or place ID')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Only the owner can update this place')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400

        try:
            # Check if place exists first
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Check if the current user is the owner of the place
            if place.owner.id != current_user_id:
                return {'error': 'Unauthorized action'}, 403
            
            place_data = api.payload

            # Validate data types for update fields
            if 'title' in place_data:
                if (not isinstance(place_data['title'], str) or
                        not place_data['title'].strip()):
                    return {'error': 'Title must be a non-empty string'}, 400

            if 'price' in place_data:
                if isinstance(place_data['price'], str):
                    try:
                        place_data['price'] = float(place_data['price'])
                    except ValueError:
                        return {'error': 'Price must be a valid number'}, 400
                elif not isinstance(place_data['price'], (int, float)):
                    return {'error': 'Price must be a number'}, 400

                if place_data['price'] <= 0:
                    return {'error': 'Price must be positive'}, 400

            if 'latitude' in place_data:
                if isinstance(place_data['latitude'], str):
                    try:
                        place_data['latitude'] = float(place_data['latitude'])
                    except ValueError:
                        return {'error': 'Latitude must be a valid number'}, \
                            400
                elif not isinstance(place_data['latitude'], (int, float)):
                    return {'error': 'Latitude must be a number'}, 400

                if not -90 <= place_data['latitude'] <= 90:
                    return {'error': 'Latitude must be between -90 and 90'}, \
                        400

            if 'longitude' in place_data:
                if isinstance(place_data['longitude'], str):
                    try:
                        place_data['longitude'] = \
                            float(place_data['longitude'])
                    except ValueError:
                        return {'error': 'Longitude must be a valid number'}, \
                            400
                elif not isinstance(place_data['longitude'], (int, float)):
                    return {'error': 'Longitude must be a number'}, 400

                if not -180 <= place_data['longitude'] <= 180:
                    return ({'error': 'Longitude must be between -180 and '
                             '180'}, 400)

            # Place was already retrieved earlier for ownership check
            if ('title' in place_data and
                    place_data['title'] != place.title):
                existing_place = facade.get_place_by_title(
                    place_data['title'])
                if existing_place:
                    return {'error': 'title already exist'}, 400

            updated_place = facade.update_place(place_id, place_data)
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner': {
                    'id': updated_place.owner.id,
                    'first_name': updated_place.owner.first_name,
                    'last_name': updated_place.owner.last_name,
                    'email': updated_place.owner.email
                },
                'description': updated_place.description,
                'amenities': [{'id': amenity.id, 'name': amenity.name}
                              for amenity in updated_place.amenities],
                'reviews': [{'id': review.id, 'text': review.text,
                             'rating': review.rating,
                             'user_id': review.user.id}
                            for review in updated_place.reviews]
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.response(200, 'Amenities retrieved successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all amenities for a place"""
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [{'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities], 200

    @api.expect(api.model('PlaceAmenityAdd', {
        'amenity_id': fields.String(required=True)
    }))
    @jwt_required()
    @api.response(200, 'Amenity added successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place or amenity not found')
    def post(self, place_id):
        """Add an amenity to a place"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner.id != current_user_id:
            return {'error': 'Forbidden - Only place owner can add amenities'}, 403
        
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400
        data = api.payload
        try:
            # Validate amenity_id field exists and is string
            if 'amenity_id' not in data:
                return {'error': 'Missing required field: amenity_id'}, 400

            if not isinstance(data['amenity_id'], str):
                return {'error': 'amenity_id must be a string'}, 400

            if not data['amenity_id'].strip():
                return {'error': 'amenity_id cannot be empty'}, 400

            success = facade.add_amenity_to_place(place_id,
                                                  data['amenity_id'])
            if success:
                return {'message': 'Amenity added successfully'}, 200
            else:
                return {'error': 'Place or amenity not found'}, 404
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500


@api.route('/<place_id>/reviews')
class PlaceReviewsList(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                'user_id': review.user.id} for review in reviews], 200
