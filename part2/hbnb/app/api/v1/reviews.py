from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        if not review_data or review_data.get('text') is None:
            return {'Bad Request': 'input data is invalid'}, 400
        
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 404
        
        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
            
        except Exception as e:
            return {'error': 'Failed to create review', 'message': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        try:
            reviews = facade.get_all_reviews()
            return [{'id': review.id, 
                     'text': review.text,
                     'rating': review.rating}
                    for review in reviews], 200
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Validate review_id is not empty
        if not review_id or review_id.strip():
            return {'error': 'Invalid review ID'}, 400
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Not found'}, 404
        return {}

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        if not review_id or review.strip() == '':
            return {'error': 'Invalid review ID'}, 400
            
        try:
            review_data = api.payload
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'review not found'}, 404

            updated_review = facade.update_review(review_id, review_data)
            return {'text': new_review.text, 'rating': new_review.rating}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if not review_id:
            return {'error': 'Invalid review ID'}, 400
        
        try:
            review_data = api.payload
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'review not found'}, 404
            
            delete_review = facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        
        except ValueError as e:
            return {'message': str(e)}, 400
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
