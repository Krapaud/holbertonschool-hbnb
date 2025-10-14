from app.models.amenity import AmenityModel
from app.models.place import PlaceModel
from app.models.review import ReviewModel
from app.models.user import UserModel
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = UserModel(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        user.validate_user_data()
        user.save()
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity

        amenity = AmenityModel(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)
    
    def get_amenity_by_name(self, amenity_name):
        # Placeholder for logic to retrieve an amenity by name
        return self.amenity_repo.get_by_attribute('name', amenity_name)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        amenity.save()
        return amenity

    def create_place(self, place_data):
    # Récupérer l'owner une seule fois
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError(f"Owner with id {place_data['owner_id']} not found")
        
        # Remplacer owner_id par l'objet owner
        place_data['owner'] = owner
        del place_data['owner_id']
        
        # Créer la place
        place = PlaceModel(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated
        # owner and amenities
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        return self.place_repo.get_by_attribute('title', title)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Si owner_id est fourni, le convertir en objet UserModel
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError(f"Owner with id {place_data['owner_id']} not found")
            place_data['owner'] = owner
            del place_data['owner_id']
        
        place.update(place_data)
        place.save()
        return place

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for
        # user_id, place_id, and rating
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        # Get user and place objects
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")

        # Create review with the expected parameters
        review = ReviewModel(text=text, rating=rating, place=place, user=user)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Retrieve all reviews for a specific place
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(review_data)
        review.save()
        return review

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        return self.review_repo.delete(review_id)
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        
        if not place or not amenity:
            return False
            
        # Vérifier si l'amenity n'est pas déjà ajoutée
        if amenity not in place.amenities:
            place.add_amenity(amenity)
            place.save()
        return True
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """Remove an amenity from a place"""
        place = self.get_place(place_id)
        if not place:
            return False
            
        # Trouver et supprimer l'amenity
        place.amenities = [a for a in place.amenities if a.id != amenity_id]
        place.save()
        return True
