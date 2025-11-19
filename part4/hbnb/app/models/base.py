#!/usr/bin/env python3
"""Base model module.

This module defines the BaseModel class which serves as the parent class
for all models in the application. It provides common attributes and methods
that are inherited by all other models.
"""
import uuid
from datetime import datetime, timezone
from app import db


class BaseModel(db.Model):
    """Abstract base model class for all database models.
    
    This class provides common attributes (id, created_at, updated_at)
    and methods (save, update) that are shared across all models.
    It uses SQLAlchemy's declarative base and should not be instantiated directly.
    
    Attributes:
        id (str): Unique identifier (UUID) for each record
        created_at (datetime): Timestamp of record creation
        updated_at (datetime): Timestamp of last update
    """
    # Prevent SQLAlchemy from creating a table for this base class
    # Only child classes will have actual database tables
    __abstract__ = True

    # Primary key: UUID stored as string for better compatibility
    id = db.Column(db.String(36), primary_key=True)
    
    # Automatic timestamp for record creation
    # Uses UTC timezone to avoid ambiguity across different servers
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    
    # Automatic timestamp for last update
    # Updated automatically on each modification via onupdate
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.
        
        Generates a UUID for the id field if not provided.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        # Generate a unique ID if not provided
        # This ensures every record has a valid UUID
        if not self.id:
            self.id = str(uuid.uuid4())

    def save(self):
        """Update the updated_at timestamp.
        
        This method should be called whenever the object is modified
        to ensure the updated_at timestamp reflects the latest change.
        """
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """Update multiple attributes from a dictionary.
        
        Only updates attributes that exist on the model.
        Automatically updates the updated_at timestamp.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
                        Example: {'first_name': 'John', 'last_name': 'Doe'}
        """
        # Iterate through the provided data dictionary
        for key, value in data.items():
            # Only update if the attribute exists on the model
            # This prevents adding arbitrary attributes
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Update the timestamp to reflect this modification
        self.save()
