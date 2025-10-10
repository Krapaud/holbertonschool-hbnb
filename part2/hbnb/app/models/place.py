from . import BaseModel

class PlaceModel(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        if len(title) < 100:
            self.title = title
        else:
            print("Required, maximum length of 100 characters.")
        self.description = description
        if price > 0:
            self.price = price
        else:
            print("price must be positive")
        if latitude > -180.0 and latitude < 180.0:
            self.latitude = latitude
        else:
            print("latitude msut be between -180.0 and 180.0")
        if longitude < 90.0 and longitude > -90.0:
            self.longitude = longitude
        else:
            print("longitude must be between -90.0 and 90.0")
        if isinstance(owner, UserModel):
            self.owner = owner
        else:
            print("The owner doesn't exist")
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
