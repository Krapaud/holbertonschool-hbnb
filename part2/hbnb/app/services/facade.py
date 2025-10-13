from app.persistence.repository import InMemoryRepository
from app.models.user import UserModel

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

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
        return user

    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass
