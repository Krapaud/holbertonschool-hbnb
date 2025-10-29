from .base import BaseModel
from .place import PlaceModel
from .user import UserModel
from app import db


class ReviewModel(BaseModel):
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    place = db.relationship("PlaceModel", back_populates="reviews")
    user = db.relationship("UserModel", back_populates="reviews")
    
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
