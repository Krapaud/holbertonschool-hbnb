from app.models.amenity import AmenityModel
from app.models.place import PlaceModel
from app.models.review import ReviewModel
from app.models.user import UserModel
from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository


class HBnBFacade:
    """
    Facade pattern: Pure business logic layer
    Coordinates operations between models and repositories
    """
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(UserModel)
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    # ==================== USER BUSINESS LOGIC ====================

    def create_user(self, user_data):
        """Business logic: Create a new user"""
        user = UserModel(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Business logic: Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Business logic: Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Business logic: Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Business logic: Update an existing user"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        user.validate_user_data()
        user.save()
        return user

    # ==================== AMENITY BUSINESS LOGIC ====================

    def create_amenity(self, amenity_data):
        """Business logic: Create a new amenity"""
        amenity = AmenityModel(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Business logic: Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, amenity_name):
        """Business logic: Retrieve an amenity by name"""
        return self.amenity_repo.get_by_attribute('name', amenity_name)

    def get_all_amenities(self):
        """Business logic: Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Business logic: Update an existing amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        amenity.save()
        return amenity

    # ==================== PLACE BUSINESS LOGIC ====================

    def create_place(self, place_data):
        """Business logic: Create a new place with owner validation"""
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner with id {} not found"
                             .format(place_data['owner_id']))

        place_data['owner'] = owner
        del place_data['owner_id']

        place = PlaceModel(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Business logic: Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        """Business logic: Retrieve a place by title"""
        return self.place_repo.get_by_attribute('title', title)

    def get_all_places(self):
        """Business logic: Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Business logic: Update an existing place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner with id {} not found"
                                 .format(place_data['owner_id']))
            place_data['owner'] = owner
            del place_data['owner_id']

        place.update(place_data)
        place.save()
        return place

    def add_amenity_to_place(self, place_id, amenity_id):
        """Business logic: Associate an amenity with a place"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if not place or not amenity:
            return False

        if amenity not in place.amenities:
            place.amenities.append(amenity)
            place.save()
        return True

    # ==================== REVIEW BUSINESS LOGIC ====================

    def create_review(self, review_data):
        """Business logic: Create a review and link it to place"""
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)

        review = ReviewModel(text=text, rating=rating, place=place, user=user)
        self.review_repo.add(review)

        place.reviews.append(review)
        place.save()
        return review

    def get_review(self, review_id):
        """Business logic: Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Business logic: Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Business logic: Retrieve all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews
                if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """Business logic: Update an existing review"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(review_data)
        review.save()
        return review

    def delete_review(self, review_id):
        """Business logic: Delete a review and remove it from place"""
        review = self.review_repo.get(review_id)
        if review:
            place = review.place
            if review in place.reviews:
                place.reviews.remove(review)
                place.save()

            self.review_repo.delete(review_id)
            return True
        return False
