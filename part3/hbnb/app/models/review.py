from .base import BaseModel
from .place import PlaceModel
from .user import User


class ReviewModel(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Text is required and cannot be empty")

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        if not isinstance(place, PlaceModel):
            raise ValueError("Place must be a valid Place instance")

        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
