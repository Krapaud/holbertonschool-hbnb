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
            # Validate required fields
            required_fields = ['text', 'rating', 'user_id', 'place_id']
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

            # Validate user_id and place_id are strings
            if not isinstance(review_data['user_id'], str):
                return {'error': 'user_id must be a string'}, 400
            if not isinstance(review_data['place_id'], str):
                return {'error': 'place_id must be a string'}, 400

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
            error_msg = str(e)
            # Check if it's a "not found" error (User/Place not found)
            if "not found" in error_msg:
                return {'error': error_msg}, 404
            # Otherwise, it's a validation error (empty text, invalid rating,
            # etc.)
            return {'error': error_msg}, 400
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
