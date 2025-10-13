from . import BaseModel


class AmenityModel(BaseModel):
    def __init__(self, name):
        super().__init__()
        if len(name) < 50:
            self.name = name
        else:
            raise ValueError ("Required, maximum length of 50 characters.")

    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass
