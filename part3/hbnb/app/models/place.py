from .base import BaseModel
from .user import UserModel
from app import db
from sqlalchemy.orm import validates

place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class PlaceModel(BaseModel):
    __tablename__ = 'places'

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner = db.relationship("UserModel", back_populates="places")
    reviews = db.relationship("ReviewModel", back_populates="place")
    amenities = db.relationship(
        "AmenityModel",
        secondary="place_amenity",
        back_populates="places"
    )

    @validates('title')
    def validate_title(self, key, title):
        if title and len(title) < 100:
            return title
        else:
            raise ValueError("Required, maximum length of 100 characters.")

    @validates('price')
    def validate_price(self, key, price):
        if price > 0:
            return price
        else:
            raise ValueError("price must be positive")

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if latitude >= -90.0 and latitude <= 90.0:
            return latitude
        else:
            raise ValueError("latitude must be between -90.0 and 90.0")

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if longitude >= -180.0 and longitude <= 180.0:
            return longitude
        else:
            raise ValueError("longitude must be between -180.0 and 180.0")

    @validates('owner')
    def validate_owner(self, key, owner):
        if isinstance(owner, UserModel):
            return owner
        else:
            raise ValueError("The owner doesn't exist")

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
