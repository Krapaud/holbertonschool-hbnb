from . import BaseModel
import re

class UserModel(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        
    
    def validate_user_data(self):
        """Validate user data"""
        if not self.first_name and len(first_name) > 50:
            raise ValueError("First name is required")
        if not self.last_name and len(last_name) > 50:
            raise ValueError("Last name is required")
        if not self.email or not self.is_valid_email(self.email):
            raise ValueError("Valid email is required")
        if not self.password or len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
    
    def is_valid_email(self, email):
        """Basic email validation"""
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def authenticate(self, email, password):
        """Authenticate user with email and password"""
        return self.email == email and self.password == password
    
    def create_profile(self):
        """Create user profile - placeholder for business logic"""
        pass
    
    def update_profile(self, data):
        """Update user profile"""
        allowed_fields = ['first_name', 'last_name', 'email']
        for key, value in data.items():
            if key in allowed_fields and hasattr(self, key):
                setattr(self, key, value)
          
    def delete_profile(self):
        """Delete user profile - placeholder for business logic"""
        pass
    
    def to_dict(self):
        """Convert user to dictionary (excluding password for security)"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        