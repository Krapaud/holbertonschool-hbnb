#!/usr/bin/env python3
"""Place model module.

This module defines the PlaceModel class which represents accommodations
that users can rent. Places can have amenities and receive reviews from users.
"""
from .base import BaseModel
from .user import UserModel
from app import db
from sqlalchemy.orm import validates

# Association table for many-to-many relationship between places and amenities
# A place can have multiple amenities, and an amenity can belong to multiple places
place_amenity = db.Table(
    'place_amenity',
    # Foreign key to places table
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    ),
    # Foreign key to amenities table
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class PlaceModel(BaseModel):
    """Place model class.
    
    Represents an accommodation (apartment, house, etc.) available for rent.
    Places are owned by users and can have multiple amenities and reviews.
    
    Attributes:
        owner_id (str): Foreign key to the user who owns this place
        title (str): Place title/name (max 50 chars)
        description (str): Detailed description of the place
        price (float): Price per night (must be positive)
        latitude (float): Geographic latitude (-90 to 90)
        longitude (float): Geographic longitude (-180 to 180)
        owner (relationship): User who owns this place
        reviews (relationship): Reviews for this place
        amenities (relationship): Amenities available at this place
    """
    __tablename__ = 'places'

    # Foreign key to users table with CASCADE delete
    # When a user is deleted, their places are also deleted
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'))
    
    # Place title/name - required field
    title = db.Column(db.String(50), nullable=False)
    
    # Detailed description - optional field
    description = db.Column(db.String, nullable=True)
    
    # Price per night - required, must be positive
    price = db.Column(db.Float, nullable=False)
    
    # GPS coordinates for location
    # Latitude: -90 (South Pole) to +90 (North Pole)
    latitude = db.Column(db.Float, nullable=False)
    
    # Longitude: -180 (International Date Line West) to +180 (East)
    longitude = db.Column(db.Float, nullable=False)

    # Many-to-one relationship: many places belong to one owner
    owner = db.relationship("UserModel", back_populates="places")
    
    # One-to-many relationship: one place can have many reviews
    # cascade="all, delete-orphan" deletes reviews when place is deleted
    reviews = db.relationship("ReviewModel", back_populates="place", cascade="all, delete-orphan")
    
    # Many-to-many relationship: places can have multiple amenities
    # Uses place_amenity association table
    amenities = db.relationship(
        "AmenityModel",
        secondary="place_amenity",
        back_populates="places"
    )

    @validates('title')
    def validate_title(self, key, title):
        """Validate place title.
        
        Args:
            key (str): Name of the field being validated
            title (str): Title to validate
            
        Returns:
            str: Validated title
            
        Raises:
            ValueError: If title is empty or exceeds 100 characters
        """
        if title and len(title) < 100:
            return title
        else:
            raise ValueError("Required, maximum length of 100 characters.")

    @validates('price')
    def validate_price(self, key, price):
        """Validate price field.
        
        Ensures price is a positive number.
        
        Args:
            key (str): Name of the field being validated
            price (float): Price to validate
            
        Returns:
            float: Validated price
            
        Raises:
            ValueError: If price is zero or negative
        """
        if price > 0:
            return price
        else:
            raise ValueError("price must be positive")

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validate latitude coordinate.
        
        Latitude must be between -90 (South Pole) and +90 (North Pole).
        
        Args:
            key (str): Name of the field being validated
            latitude (float): Latitude to validate
            
        Returns:
            float: Validated latitude
            
        Raises:
            ValueError: If latitude is outside valid range
        """
        if latitude >= -90.0 and latitude <= 90.0:
            return latitude
        else:
            raise ValueError("latitude must be between -90.0 and 90.0")

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validate longitude coordinate.
        
        Longitude must be between -180 and +180 degrees.
        
        Args:
            key (str): Name of the field being validated
            longitude (float): Longitude to validate
            
        Returns:
            float: Validated longitude
            
        Raises:
            ValueError: If longitude is outside valid range
        """
        if longitude >= -180.0 and longitude <= 180.0:
            return longitude
        else:
            raise ValueError("longitude must be between -180.0 and 180.0")

    @validates('owner')
    def validate_owner(self, key, owner):
        """Validate owner relationship.
        
        Ensures the owner is a valid UserModel instance.
        
        Args:
            key (str): Name of the field being validated
            owner (UserModel): Owner to validate
            
        Returns:
            UserModel: Validated owner
            
        Raises:
            ValueError: If owner is not a UserModel instance
        """
        if isinstance(owner, UserModel):
            return owner
        else:
            raise ValueError("The owner doesn't exist")

    def add_review(self, review):
        """Add a review to this place.
        
        Args:
            review (ReviewModel): Review object to add
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place.
        
        Args:
            amenity (AmenityModel): Amenity object to add
        """
        self.amenities.append(amenity)
