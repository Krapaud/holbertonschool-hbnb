from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        place_data = api.payload
        try:
            # Vérification d'unicité par titre
            existing_place = facade.get_place_by_title(place_data['title'])
            if existing_place:
                return {'error': 'Place already registered'}, 400
            new_place = facade.create_place(place_data)
            return {'id': new_place.id, 'title': new_place.title,
                    'price': new_place.price, 'latitude': new_place.latitude,
                    'longitude': new_place.longitude, 
                    'owner': {'id': new_place.owner.id, 'first_name': new_place.owner.first_name, 
                             'last_name': new_place.owner.last_name, 'email': new_place.owner.email},
                    'description': new_place.description,
                    'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in new_place.amenities],
                    'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating,
                               'user_id': review.user_id} for review in new_place.reviews]}, 201
        except ValueError as e:
            # Handle validation errors from the model
            return {'message': str(e)}, 400
        except Exception as e:
            # Handle any other unexpected errors
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Utilise la façade pour récupérer toutes les places
        places = facade.get_all_places()
        result = []
        for place in places:
            place_dict = {
                'id': place.id, 
                'title': place.title, 
                'price': place.price,
                'latitude': place.latitude, 
                'longitude': place.longitude,
                'description': place.description
            }
            # Inclure l'owner seulement s'il existe et le sérialiser correctement
            if hasattr(place, 'owner') and place.owner:
                place_dict['owner'] = {
                    'id': place.owner.id, 
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name, 
                    'email': place.owner.email
                }
            # Inclure amenities et reviews
            place_dict['amenities'] = [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
            place_dict['reviews'] = [{'id': review.id, 'text': review.text, 'rating': review.rating,
                                    'user_id': review.user_id} for review in place.reviews]
            result.append(place_dict)
        return result, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Validate place_id is not empty
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400
            
        # Utilise la façade pour récupérer une place par ID
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 'title': place.title, 'price': place.price,
                'latitude': place.latitude, 'longitude': place.longitude,
                'description': place.description, 
                'owner': {'id': place.owner.id, 'first_name': place.owner.first_name,
                         'last_name': place.owner.last_name, 'email': place.owner.email},
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities],
                'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating, 
                           'user_id': review.user_id} for review in place.reviews]}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data or place ID')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place's information"""
        # Validate place_id is not empty
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400
            
        # Placeholder for the logic to update a place by ID
        try:
            place_data = api.payload
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'place not found'}, 404
            if 'title' in place_data and place_data['title'] != place.title:
                existing_place = facade.get_place_by_title(place_data['title'])
                if existing_place:
                    return {'error': 'title already exist'}, 400

            updated_place = facade.update_place(place_id, place_data)
            return {'id': updated_place.id, 'title': updated_place.title,
                    'price': updated_place.price, 'latitude': updated_place.latitude,
                    'longitude': updated_place.longitude, 
                    'owner': {'id': updated_place.owner.id, 'first_name': updated_place.owner.first_name,
                             'last_name': updated_place.owner.last_name, 'email': updated_place.owner.email},
                    'description': updated_place.description,
                    'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in updated_place.amenities],
                    'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating,
                               'user_id': review.user_id} for review in updated_place.reviews]}, 200
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
        # Validate place_id is not empty
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400
            
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities], 200
    
    @api.expect(api.model('PlaceAmenityAdd', {'amenity_id': fields.String(required=True)}))
    @api.response(200, 'Amenity added successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place or amenity not found')
    def post(self, place_id):
        """Add an amenity to a place"""
        # Validate place_id is not empty
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400
            
        data = api.payload
        try:
            success = facade.add_amenity_to_place(place_id, data['amenity_id'])
            if success:
                return {'message': 'Amenity added successfully'}, 200
            else:
                return {'error': 'Place or amenity not found'}, 404
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(400, 'Invalid place ID')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        # Validate place_id is not empty
        if not place_id or place_id.strip() == '':
            return {'error': 'Invalid place ID'}, 400
            
        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                'user_id': review.user_id} for review in reviews], 200
