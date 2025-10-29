from .base import BaseModel
from app import db


class AmenityModel(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = db.relationship(
        "PlaceModel",
        secondary="place_amenity",
        back_populates="amenities"
    )

    def __init__(self, name):
        super().__init__()
        self.validate_name(name)
        self.name = name

    def validate_name(self, name):
        """Validate amenity name"""
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string")

        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")

        if len(name) > 50:
            raise ValueError("Name must not exceed 50 characters")

    def update(self, data):
        """Update amenity attributes"""
        if 'name' in data:
            self.validate_name(data['name'])
            self.name = data['name'].strip()

        # Update timestamp
        super().save()

    def save(self):
        """Save the amenity (update timestamp)"""
        super().save()
