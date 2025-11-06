from .base import BaseModel
from .place import PlaceModel
from .user import UserModel
from app import db
from sqlalchemy.orm import validates


class ReviewModel(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place'),
    )

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))

    place = db.relationship("PlaceModel", back_populates="reviews")
    user = db.relationship("UserModel", back_populates="reviews")

    @validates('text')
    def validate_text(self, key, text):
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Text is required and cannot be empty")
        return text

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @validates('place')
    def validate_place(self, key, place):
        if not isinstance(place, PlaceModel):
            raise ValueError("Place must be a valid Place instance")
        return place

    @validates('user')
    def validate_user(self, key, user):
        if not isinstance(user, UserModel):
            raise ValueError("User must be a valid User instance")
        return user
