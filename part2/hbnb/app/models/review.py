from . import BaseModel
from .place import PlaceModel
from .user import UserModel


class ReviewModel(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Text is required and cannot be empty")

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if not isinstance(place, PlaceModel):
            raise ValueError("Place must be a valid Place instance")

        if not isinstance(user, UserModel):
            raise ValueError("User must be a valid User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        """Convert the ReviewModel instance to a dictionary for API responses"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
