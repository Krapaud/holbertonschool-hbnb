from app.models.user import UserModel

def test_user_creation():
    user = UserModel(first_name="John", last_name="Doe", email="john.doe@example.com", password="password123")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

test_user_creation()

from app.models.place import PlaceModel
from app.models.amenity import AmenityModel

def test_place_creation():
    owner = UserModel(first_name="Alice", last_name="Smith", email="alice.smith@example.com", password="password123")
    place = PlaceModel(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding an amenity
    amenity = AmenityModel(name="Wi-Fi")
    place.add_amenity(amenity)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wi-Fi"
    print("Place creation and relationship test passed!")

test_place_creation()

def test_amenity_creation():
    amenity = AmenityModel(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()
