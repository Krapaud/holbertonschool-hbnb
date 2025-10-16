from base import BaseModel
from user import UserModel


class PlaceModel(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner,
                 description=None):
        super().__init__()
        if title and len(title) < 100:
            self.title = title
        else:
            raise ValueError("Required, maximum length of 100 characters.")
        self.description = description
        if price > 0:
            self.price = price
        else:
            raise ValueError("price must be positive")
        if latitude >= -90.0 and latitude <= 90.0:
            self.latitude = latitude
        else:
            raise ValueError("latitude must be between -90.0 and 90.0")
        if longitude >= -180.0 and longitude <= 180.0:
            self.longitude = longitude
        else:
            raise ValueError("longitude must be between -180.0 and 180.0")
        if isinstance(owner, UserModel):
            self.owner = owner
        else:
            raise ValueError("The owner doesn't exist")
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
