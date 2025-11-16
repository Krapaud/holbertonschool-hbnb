from .base import BaseModel
from app import db
from sqlalchemy.orm import validates


class AmenityModel(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = db.relationship(
        "PlaceModel",
        secondary="place_amenity",
        back_populates="amenities"
    )

    @validates('name')
    def validate_name(self, key, name):
        """Validate amenity name"""
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string")

        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")

        if len(name) > 50:
            raise ValueError("Name must not exceed 50 characters")

        return name

    def update(self, data):
        """Update amenity attributes"""
        if 'name' in data:
            self.name = data['name']

        # Update timestamp
        super().save()

    def save(self):
        """Save the amenity (update timestamp)"""
        super().save()
