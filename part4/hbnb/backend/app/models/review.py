#!/usr/bin/env python3
"""Review model module.

This module defines the ReviewModel class which represents user reviews
for places. Each user can write one review per place.
"""
from .base import BaseModel
from .place import PlaceModel
from .user import UserModel
from app import db
from sqlalchemy.orm import validates


class ReviewModel(BaseModel):
    """Review model class.
    
    Represents a user's review of a place. Each user can only write
    one review per place (enforced by unique constraint).
    
    Attributes:
        text (str): Review text/comment
        rating (int): Rating from 1 to 5 stars
        place_id (str): Foreign key to the place being reviewed
        user_id (str): Foreign key to the user writing the review
        place (relationship): Place being reviewed
        user (relationship): User who wrote the review
    """
    __tablename__ = 'reviews'
    
    # Unique constraint: one user can only review a place once
    # Prevents duplicate reviews from the same user for the same place
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place'),
    )

    # Review text - required field for the review content
    text = db.Column(db.Text, nullable=False)
    
    # Rating from 1 (worst) to 5 (best) stars
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign key to places table with CASCADE delete
    # When a place is deleted, its reviews are also deleted
    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'))
    
    # Foreign key to users table with CASCADE delete
    # When a user is deleted, their reviews are also deleted
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'))

    # Many-to-one relationship: many reviews belong to one place
    place = db.relationship("PlaceModel", back_populates="reviews")
    
    # Many-to-one relationship: many reviews are written by one user
    user = db.relationship("UserModel", back_populates="reviews")

    @validates('text')
    def validate_text(self, key, text):
        """Validate review text.
        
        Ensures review text is provided and not empty.
        
        Args:
            key (str): Name of the field being validated
            text (str): Review text to validate
            
        Returns:
            str: Validated review text
            
        Raises:
            ValueError: If text is None, not a string, or empty after stripping
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Text is required and cannot be empty")
        return text

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate review rating.
        
        Ensures rating is an integer between 1 and 5 (inclusive).
        
        Args:
            key (str): Name of the field being validated
            rating (int): Rating value to validate
            
        Returns:
            int: Validated rating
            
        Raises:
            ValueError: If rating is not an integer or outside 1-5 range
        """
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @validates('place')
    def validate_place(self, key, place):
        """Validate place relationship.
        
        Ensures the place is a valid PlaceModel instance.
        
        Args:
            key (str): Name of the field being validated
            place (PlaceModel): Place to validate
            
        Returns:
            PlaceModel: Validated place
            
        Raises:
            ValueError: If place is not a PlaceModel instance
        """
        if not isinstance(place, PlaceModel):
            raise ValueError("Place must be a valid Place instance")
        return place

    @validates('user')
    def validate_user(self, key, user):
        """Validate user relationship.
        
        Ensures the user is a valid UserModel instance.
        
        Args:
            key (str): Name of the field being validated
            user (UserModel): User to validate
            
        Returns:
            UserModel: Validated user
            
        Raises:
            ValueError: If user is not a UserModel instance
        """
        if not isinstance(user, UserModel):
            raise ValueError("User must be a valid User instance")
        return user
