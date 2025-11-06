from .base import BaseModel
import re


class UserModel(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate_user_data()

    def validate_user_data(self):
        """Validate user data"""
        if (not self.first_name or len(self.first_name) > 50 or
            len(self.first_name.strip()) == 0):
            raise ValueError("First name is required and must be <= 50 chars")
        if (not self.last_name or len(self.last_name) > 50 or
            len(self.last_name.strip()) == 0):
            raise ValueError("Last name is required and must be <= 50 chars")
        if not self.email or not self.is_valid_email(self.email):
            raise ValueError("Valid email is required")

    def is_valid_email(self, email):
        """Basic email validation"""
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
