from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
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
        try:
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
            return {'error': str(e)}, 404  # Not found for User/Place
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
    def put(self, review_id):
        """Update a review's information"""
        if not review_id or not review_id.strip():
            return {'error': 'Invalid review ID'}, 400

        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
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
    def delete(self, review_id):
        """Delete a review"""
        if not review_id or not review_id.strip():
            return {'error': 'Invalid review ID'}, 400

        try:
            if facade.delete_review(review_id):
                return {'message': 'Review deleted successfully'}, 200
            else:
                return {'error': 'Review not found'}, 404

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


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
                'user_id': review.user.id} for review in reviews], 200
