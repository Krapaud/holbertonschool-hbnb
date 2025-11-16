from .base import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import validates
import re


class UserModel(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship("PlaceModel", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("ReviewModel", back_populates="user", cascade="all, delete-orphan")

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        """Validate first name"""
        max_length = 50
        if (not first_name or len(first_name) > max_length or
                len(first_name.strip()) == 0):
            raise ValueError("First name is required and must be <= 50 chars")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        """Validate last name"""
        if not last_name or len(last_name) > 50 or len(last_name.strip()) == 0:
            raise ValueError("Last name is required and must be <= 50 chars")
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        """Validate email"""
        if not email or not self.is_valid_email(email):
            raise ValueError("Valid email is required")
        return email

    def is_valid_email(self, email):
        """Basic email validation"""
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
