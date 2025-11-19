#!/usr/bin/env python3
"""Amenity model module.

This module defines the AmenityModel class which represents amenities
that can be associated with places (WiFi, Pool, Air Conditioning, etc.).
"""
from .base import BaseModel
from app import db
from sqlalchemy.orm import validates


class AmenityModel(BaseModel):
    """Amenity model class.
    
    Represents an amenity that places can offer (e.g., WiFi, Swimming Pool).
    Each amenity has a unique name and can be associated with multiple places.
    
    Attributes:
        name (str): Unique name of the amenity (max 50 chars)
        places (relationship): Places that have this amenity
    """
    __tablename__ = 'amenities'

    # Amenity name - must be unique across all amenities
    # Examples: "WiFi", "Swimming Pool", "Air Conditioning"
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Many-to-many relationship: amenities can belong to multiple places
    # Uses place_amenity association table
    places = db.relationship(
        "PlaceModel",
        secondary="place_amenity",
        back_populates="amenities"
    )

    @validates('name')
    def validate_name(self, key, name):
        """Validate amenity name.
        
        Ensures name is a non-empty string within length limit.
        
        Args:
            key (str): Name of the field being validated
            name (str): Name to validate
            
        Returns:
            str: Validated and trimmed name
            
        Raises:
            ValueError: If name is None, not a string, empty, or exceeds 50 chars
        """
        # Check if name exists and is a string
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string")

        # Remove leading/trailing whitespace
        name = name.strip()
        
        # Check if name is empty after stripping whitespace
        if not name:
            raise ValueError("Name cannot be empty")

        # Check length constraint
        if len(name) > 50:
            raise ValueError("Name must not exceed 50 characters")

        return name

    def update(self, data):
        """Update amenity attributes from dictionary.
        
        Currently only supports updating the name field.
        Automatically updates the timestamp.
        
        Args:
            data (dict): Dictionary containing fields to update
                        Example: {'name': 'New Amenity Name'}
        """
        # Update name if provided in data dictionary
        if 'name' in data:
            self.name = data['name']

        # Update the updated_at timestamp
        super().save()

    def save(self):
        """Save the amenity and update timestamp.
        
        Updates the updated_at timestamp to reflect the latest modification.
        """
        super().save()
