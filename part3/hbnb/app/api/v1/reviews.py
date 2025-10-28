from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data, cannot review own place, or already reviewed')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """Register a new review"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        
        review_data = api.payload
        try:
            # Validate required fields
            required_fields = ['text', 'rating', 'place_id']
            for field in required_fields:
                if field not in review_data:
                    return {'error': f'Missing required field: {field}'}, 400

            # Validate text is string and not empty
            if not isinstance(review_data['text'], str):
                return {'error': 'Text must be a string'}, 400
            if not review_data['text'].strip():
                return {'error': 'Text cannot be empty'}, 400

            # Validate rating is integer and in range
            if not isinstance(review_data['rating'], int):
                return {'error': 'Rating must be an integer'}, 400
            if not 1 <= review_data['rating'] <= 5:
                return {'error': 'Rating must be between 1 and 5'}, 400

            # Validate place_id is string
            if not isinstance(review_data['place_id'], str):
                return {'error': 'place_id must be a string'}, 400

            # Add the authenticated user_id to the review data
            review_data['user_id'] = current_user_id

            # Check if user exists
            user = facade.get_user(current_user_id)
            if not user:
                return {'error': 'User not found'}, 404

            # Check if place exists
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if user is trying to review their own place
            if place.owner.id == current_user_id:
                return {'error': 'You cannot review your own place.'}, 400

            # Check if user has already reviewed this place
            existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
            for review in existing_reviews:
                if review.user.id == current_user_id:
                    return {'error': 'You have already reviewed this place.'}, 400

            new_review = facade.create_review(review_data)
            return {
                'message': 'Review successfully created',
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to create review', 'details': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        try:
            reviews = facade.get_all_reviews()
            return [{'id': review.id,
                     'text': review.text,
                     'rating': review.rating,
                     'user_id': review.user.id,
                     'place_id': review.place.id
                     }
                    for review in reviews], 200
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Validate review_id is not empty
        if not review_id or not review_id.strip():
            return {'error': 'Invalid review ID'}, 400
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Not the review owner')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not review_id or not review_id.strip():
            return {'error': 'Invalid review ID'}, 400

        try:
            # Check if the review exists
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            # Check if the current user is the owner of the review (admins can bypass)
            if not is_admin and review.user.id != current_user_id:
                return {'error': 'Unauthorized action.'}, 403

            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            return {
                'message': 'Review updated successfully',
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Not the review owner')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not review_id or not review_id.strip():
            return {'error': 'Invalid review ID'}, 400

        try:
            # Check if the review exists
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            # Check if the current user is the owner of the review (admins can bypass)
            if not is_admin and review.user.id != current_user_id:
                return {'error': 'Unauthorized action.'}, 403
            
            if facade.delete_review(review_id):
                return {'message': 'Review deleted successfully'}, 200
            else:
                return {'error': 'Review not found'}, 404

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
