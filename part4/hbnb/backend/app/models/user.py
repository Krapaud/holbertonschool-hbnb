#!/usr/bin/env python3
"""User model module.

This module defines the UserModel class which represents users in the system.
Users can create places and write reviews. The model includes validation
for email format and password hashing for security.
"""
from .base import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import validates
import re


class UserModel(BaseModel):
    """User model class.
    
    Represents a user in the HBnB system. Users can own places and write reviews.
    Includes email validation and password hashing for security.
    
    Attributes:
        first_name (str): User's first name (max 50 chars)
        last_name (str): User's last name (max 50 chars)
        email (str): User's email address (must be unique and valid format)
        password (str): Hashed password (max 128 chars)
        is_admin (bool): Whether the user has admin privileges
        places (relationship): Places owned by this user
        reviews (relationship): Reviews written by this user
    """
    __tablename__ = 'users'

    # User's first name - required field with max length
    first_name = db.Column(db.String(50), nullable=False)
    
    # User's last name - required field with max length
    last_name = db.Column(db.String(50), nullable=False)
    
    # Email address - must be unique across all users
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    # Hashed password - never store plain text passwords
    password = db.Column(db.String(128), nullable=False)
    
    # Admin flag - controls access to privileged operations
    is_admin = db.Column(db.Boolean, default=False)

    # One-to-many relationship: one user can own multiple places
    # cascade="all, delete-orphan" ensures places are deleted when user is deleted
    places = db.relationship("PlaceModel", back_populates="owner", cascade="all, delete-orphan")
    
    # One-to-many relationship: one user can write multiple reviews
    # cascade="all, delete-orphan" ensures reviews are deleted when user is deleted
    reviews = db.relationship("ReviewModel", back_populates="user", cascade="all, delete-orphan")

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        """Validate first name field.
        
        Ensures first name is provided, not empty, and within length limit.
        
        Args:
            key (str): Name of the field being validated
            first_name (str): The first name value to validate
            
        Returns:
            str: The validated first name
            
        Raises:
            ValueError: If first name is empty, None, or exceeds 50 characters
        """
        max_length = 50
        if (not first_name or len(first_name) > max_length or
                len(first_name.strip()) == 0):
            raise ValueError("First name is required and must be <= 50 chars")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        """Validate last name field.
        
        Ensures last name is provided, not empty, and within length limit.
        
        Args:
            key (str): Name of the field being validated
            last_name (str): The last name value to validate
            
        Returns:
            str: The validated last name
            
        Raises:
            ValueError: If last name is empty, None, or exceeds 50 characters
        """
        if not last_name or len(last_name) > 50 or len(last_name.strip()) == 0:
            raise ValueError("Last name is required and must be <= 50 chars")
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        """Validate email field.
        
        Ensures email is provided and matches a valid email format.
        
        Args:
            key (str): Name of the field being validated
            email (str): The email value to validate
            
        Returns:
            str: The validated email
            
        Raises:
            ValueError: If email is empty, None, or has invalid format
        """
        if not email or not self.is_valid_email(email):
            raise ValueError("Valid email is required")
        return email

    def is_valid_email(self, email):
        """Check if email format is valid.
        
        Uses regex pattern to validate email format.
        Pattern checks for: username@domain.extension
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email matches valid format, False otherwise
        """
        # Regex pattern for basic email validation
        # Format: alphanumeric@alphanumeric.letters
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def hash_password(self, password):
        """Hash and store the user's password.
        
        Uses bcrypt to securely hash the password before storing.
        The original password is never stored in plain text.
        
        Args:
            password (str): Plain text password to hash
        """
        # Generate bcrypt hash and store as UTF-8 string
        # bcrypt automatically handles salt generation
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a password against the stored hash.
        
        Used during login to check if provided password matches.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches the hash, False otherwise
        """
        # bcrypt handles the comparison securely
        # Returns True if password matches, False otherwise
        return bcrypt.check_password_hash(self.password, password)
