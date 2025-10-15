"""
Comprehensive test suite for HBNB models
Tests cover creation, validation, relationships, and edge cases
"""

import time
from datetime import datetime

from app.models.amenity import AmenityModel
from app.models.place import PlaceModel
from app.models.user import UserModel

# Color codes for better output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

test_results = {"passed": 0, "failed": 0}


def run_test(test_name, test_func):
    """Helper function to run tests and track results"""
    try:
        test_func()
        print(f"{GREEN}✓{RESET} {test_name}")
        test_results["passed"] += 1
        return True
    except AssertionError as e:
        print(f"{RED}✗{RESET} {test_name}: {str(e)}")
        test_results["failed"] += 1
        return False
    except Exception as e:
        print(f"{RED}✗{RESET} {test_name}: Unexpected error - {str(e)}")
        test_results["failed"] += 1
        return False


# ==================== USER MODEL TESTS ====================
print(f"\n{BLUE}{'=' * 60}{RESET}")
print(f"{BLUE}USER MODEL TESTS{RESET}")
print(f"{BLUE}{'=' * 60}{RESET}\n")


def test_user_basic_creation():
    """Test basic user creation with all required fields"""
    user = UserModel(first_name="John", last_name="Doe",
                     email="john.doe@example.com")
    assert user.first_name == "John", "First name mismatch"
    assert user.last_name == "Doe", "Last name mismatch"
    assert user.email == "john.doe@example.com", "Email mismatch"
    assert user.is_admin is False, "Default admin status should be False"


run_test("User basic creation", test_user_basic_creation)


def test_user_admin_creation():
    """Test user creation with admin privileges"""
    admin = UserModel(first_name="Admin", last_name="User",
                      email="admin@example.com", is_admin=True)
    assert admin.is_admin is True, "Admin status should be True"


run_test("User admin creation", test_user_admin_creation)


def test_user_has_id():
    """Test that user gets unique ID from BaseModel"""
    user1 = UserModel(first_name="User", last_name="One",
                      email="user1@example.com")
    user2 = UserModel(first_name="User", last_name="Two",
                      email="user2@example.com")
    assert hasattr(user1, 'id'), "User should have id attribute"
    assert user1.id != user2.id, "Users should have unique IDs"


run_test("User unique ID generation", test_user_has_id)


def test_user_timestamps():
    """Test that user has created_at and updated_at timestamps"""
    user = UserModel(first_name="John", last_name="Doe",
                     email="john@example.com")
    assert hasattr(user, 'created_at'), "User should have created_at"
    assert hasattr(user, 'updated_at'), "User should have updated_at"
    assert isinstance(
        user.created_at, datetime), "created_at should be datetime"
    assert isinstance(
        user.updated_at, datetime), "updated_at should be datetime"


run_test("User timestamp creation", test_user_timestamps)


def test_user_update():
    """Test user update functionality"""
    user = UserModel(first_name="John", last_name="Doe",
                     email="john@example.com")
    old_updated_at = user.updated_at
    time.sleep(0.01)  # Small delay to ensure timestamp difference
    user.update({"first_name": "Jane", "last_name": "Smith"})
    assert user.first_name == "Jane", "First name should be updated"
    assert user.last_name == "Smith", "Last name should be updated"
    assert user.updated_at > old_updated_at, "updated_at should be refreshed"


run_test("User update method", test_user_update)


def test_user_email_validation():
    """Test email validation method"""
    user = UserModel(first_name="Test", last_name="User",
                     email="valid@email.com")
    assert user.is_valid_email(
        "test@example.com") is True, "Valid email should pass"
    assert user.is_valid_email(
        "invalid.email") is False, "Invalid email should fail"
    assert user.is_valid_email(
        "no@domain") is False, "Email without TLD should fail"
    assert user.is_valid_email(
        "@example.com") is False, "Email without local part should fail"


run_test("User email validation", test_user_email_validation)


def test_user_validation_errors():
    """Test that invalid user data raises errors"""
    try:
        # Empty first name
        user = UserModel(
            first_name="",
            last_name="Doe",
            email="test@example.com")
        assert False, "Should raise ValueError for empty first name"
    except ValueError as e:
        assert "First name" in str(e), "Error should mention first name"

    try:
        # Invalid email
        user = UserModel(
            first_name="John",
            last_name="Doe",
            email="invalid-email")
        assert False, "Should raise ValueError for invalid email"
    except ValueError as e:
        assert "email" in str(e).lower(), "Error should mention email"


run_test("User validation errors", test_user_validation_errors)


def test_user_name_length_validation():
    """Test name length validation"""
    try:
        # First name too long (> 50 characters)
        long_name = "A" * 51
        user = UserModel(
            first_name=long_name,
            last_name="Doe",
            email="test@example.com")
        assert False, "Should raise ValueError for name > 50 chars"
    except ValueError as e:
        assert "50" in str(e), "Error should mention character limit"


run_test("User name length validation", test_user_name_length_validation)

# ==================== PLACE MODEL TESTS ====================
print(f"\n{BLUE}{'=' * 60}{RESET}")
print(f"{BLUE}PLACE MODEL TESTS{RESET}")
print(f"{BLUE}{'=' * 60}{RESET}\n")


def test_place_basic_creation():
    """Test basic place creation"""
    owner = UserModel(first_name="Alice", last_name="Smith",
                      email="alice@example.com")
    place = PlaceModel(
        title="Cozy Apartment",
        description="A nice place",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner)
    assert place.title == "Cozy Apartment", "Title mismatch"
    assert place.description == "A nice place", "Description mismatch"
    assert place.price == 100, "Price mismatch"
    assert place.latitude == 37.7749, "Latitude mismatch"
    assert place.longitude == -122.4194, "Longitude mismatch"
    assert place.owner == owner, "Owner mismatch"


run_test("Place basic creation", test_place_basic_creation)


def test_place_coordinates_validation():
    """Test place coordinate boundaries"""
    owner = UserModel(first_name="Owner", last_name="Test",
                      email="owner@example.com")

    # Valid coordinates
    place1 = PlaceModel(title="Valid Place", price=50,
                        latitude=0, longitude=0, owner=owner)
    assert hasattr(place1, 'latitude'), "Valid coordinates should be accepted"

    # Edge cases
    place2 = PlaceModel(title="North Pole", price=50,
                        latitude=90.0, longitude=0, owner=owner)
    assert place2.latitude == 90.0, "North pole latitude should be valid"

    place3 = PlaceModel(title="South Pole", price=50,
                        latitude=-90.0, longitude=0, owner=owner)
    assert place3.latitude == -90.0, "South pole latitude should be valid"


run_test("Place coordinate validation", test_place_coordinates_validation)


def test_place_amenities_relationship():
    """Test adding multiple amenities to a place"""
    owner = UserModel(first_name="Owner", last_name="Test",
                      email="owner@example.com")
    place = PlaceModel(title="Luxury Villa", price=500,
                       latitude=40.7128, longitude=-74.0060, owner=owner)

    wifi = AmenityModel(name="Wi-Fi")
    pool = AmenityModel(name="Swimming Pool")
    gym = AmenityModel(name="Gym")

    place.add_amenity(wifi)
    place.add_amenity(pool)
    place.add_amenity(gym)

    assert len(place.amenities) == 3, "Should have 3 amenities"
    assert wifi in place.amenities, "Wi-Fi should be in amenities"
    assert pool in place.amenities, "Pool should be in amenities"
    assert gym in place.amenities, "Gym should be in amenities"


run_test("Place multiple amenities", test_place_amenities_relationship)


def test_place_reviews_list():
    """Test that place has reviews list"""
    owner = UserModel(first_name="Owner", last_name="Test",
                      email="owner@example.com")
    place = PlaceModel(title="Test Place", price=100,
                       latitude=0, longitude=0, owner=owner)
    assert hasattr(place, 'reviews'), "Place should have reviews list"
    assert isinstance(place.reviews, list), "Reviews should be a list"
    assert len(place.reviews) == 0, "New place should have empty reviews"


run_test("Place reviews list initialization", test_place_reviews_list)


def test_place_price_validation():
    """Test that positive price is required"""
    owner = UserModel(first_name="Owner", last_name="Test",
                      email="owner@example.com")
    place = PlaceModel(title="Expensive Place", price=1000,
                       latitude=0, longitude=0, owner=owner)
    assert place.price == 1000, "Positive price should be accepted"


run_test("Place positive price validation", test_place_price_validation)


def test_place_has_unique_id():
    """Test that places get unique IDs"""
    owner = UserModel(first_name="Owner", last_name="Test",
                      email="owner@example.com")
    place1 = PlaceModel(title="Place 1", price=100,
                        latitude=0, longitude=0, owner=owner)
    place2 = PlaceModel(title="Place 2", price=200,
                        latitude=10, longitude=10, owner=owner)
    assert place1.id != place2.id, "Places should have unique IDs"


run_test("Place unique ID generation", test_place_has_unique_id)

# ==================== AMENITY MODEL TESTS ====================
print(f"\n{BLUE}{'=' * 60}{RESET}")
print(f"{BLUE}AMENITY MODEL TESTS{RESET}")
print(f"{BLUE}{'=' * 60}{RESET}\n")


def test_amenity_basic_creation():
    """Test basic amenity creation"""
    amenity = AmenityModel(name="Wi-Fi")
    assert amenity.name == "Wi-Fi", "Amenity name mismatch"


run_test("Amenity basic creation", test_amenity_basic_creation)


def test_amenity_has_id():
    """Test that amenity gets unique ID"""
    amenity1 = AmenityModel(name="Wi-Fi")
    amenity2 = AmenityModel(name="Pool")
    assert hasattr(amenity1, 'id'), "Amenity should have id"
    assert amenity1.id != amenity2.id, "Amenities should have unique IDs"


run_test("Amenity unique ID generation", test_amenity_has_id)


def test_amenity_various_names():
    """Test amenities with different names"""
    amenities = [
        AmenityModel(name="Wi-Fi"),
        AmenityModel(name="Air Conditioning"),
        AmenityModel(name="Kitchen"),
        AmenityModel(name="Parking"),
        AmenityModel(name="Pet-Friendly")
    ]
    names = [a.name for a in amenities]
    assert len(names) == 5, "Should create 5 amenities"
    assert "Wi-Fi" in names, "Wi-Fi should be in names"
    assert "Pet-Friendly" in names, "Pet-Friendly should be in names"


run_test("Amenity various names", test_amenity_various_names)

# ==================== USER LIST TESTS ====================
print(f"\n{BLUE}{'=' * 60}{RESET}")
print(f"{BLUE}USER LIST TESTS{RESET}")
print(f"{BLUE}{'=' * 60}{RESET}\n")


def test_get_all_users_empty():
    """Test getting all users when repository is empty"""
    from app.services.facade import HBnBFacade
    facade = HBnBFacade()
    users = facade.get_all_users()
    assert isinstance(users, list), "Should return a list"
    assert len(users) == 0, "Empty repository should return empty list"


run_test("Get all users - empty repository", test_get_all_users_empty)


def test_get_all_users_with_data():
    """Test getting all users when repository has data"""
    from app.services.facade import HBnBFacade
    facade = HBnBFacade()

    # Create test users
    user1_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"}
    user2_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com"}
    user3_data = {
        "first_name": "Bob",
        "last_name": "Wilson",
        "email": "bob@example.com"}

    # Add users to facade
    user1 = facade.create_user(user1_data)
    user2 = facade.create_user(user2_data)
    user3 = facade.create_user(user3_data)

    # Get all users
    users = facade.get_all_users()

    assert isinstance(users, list), "Should return a list"
    assert len(users) == 3, "Should return 3 users"

    # Check if all users are in the list
    user_emails = [user.email for user in users]
    assert "john@example.com" in user_emails, "John should be in the list"
    assert "jane@example.com" in user_emails, "Jane should be in the list"
    assert "bob@example.com" in user_emails, "Bob should be in the list"

    # Check user properties
    for user in users:
        assert hasattr(user, 'id'), "User should have id"
        assert hasattr(user, 'first_name'), "User should have first_name"
        assert hasattr(user, 'last_name'), "User should have last_name"
        assert hasattr(user, 'email'), "User should have email"
        assert hasattr(user, 'created_at'), "User should have created_at"
        assert hasattr(user, 'updated_at'), "User should have updated_at"


run_test("Get all users - with data", test_get_all_users_with_data)


def test_get_all_users_return_format():
    """Test that get_all_users returns proper user objects"""
    from app.services.facade import HBnBFacade
    facade = HBnBFacade()

    # Create a test user
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com"}
    created_user = facade.create_user(user_data)

    # Get all users
    users = facade.get_all_users()

    assert len(users) == 1, "Should have one user"
    returned_user = users[0]

    # Check that returned user is the same as created user
    assert returned_user.id == created_user.id, "User ID should match"
    assert (returned_user.first_name == created_user.first_name,
            "First name should match")
    assert (returned_user.last_name == created_user.last_name,
            "Last name should match")
    assert returned_user.email == created_user.email, "Email should match"
    assert (returned_user.is_admin == created_user.is_admin,
            "Admin status should match")


run_test("Get all users - return format", test_get_all_users_return_format)


def test_get_all_users_after_operations():
    """Test get_all_users after various operations (create, update, etc.)"""
    from app.services.facade import HBnBFacade
    facade = HBnBFacade()

    # Create initial users
    user1 = facade.create_user({
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com"
    })
    user2 = facade.create_user({
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob@example.com"
    })

    # Check initial count
    users = facade.get_all_users()
    assert len(users) == 2, "Should have 2 users initially"

    # Update a user
    facade.update_user(user1.id, {"first_name": "Alice Updated"})

    # Check that list still has 2 users and user is updated
    users = facade.get_all_users()
    assert len(users) == 2, "Should still have 2 users after update"

    updated_user = next((u for u in users if u.id == user1.id), None)
    assert updated_user is not None, "Updated user should be in the list"
    assert updated_user.first_name == "Alice Updated", "User should be updated"

    # Add another user
    user3 = facade.create_user({
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com"
    })

    # Final check
    users = facade.get_all_users()
    assert len(users) == 3, "Should have 3 users after adding another"

    emails = [user.email for user in users]
    assert "alice@example.com" in emails, "Alice should be in final list"
    assert "bob@example.com" in emails, "Bob should be in final list"
    assert "charlie@example.com" in emails, "Charlie should be in final list"


run_test("Get all users - after operations",
         test_get_all_users_after_operations)

# ==================== INTEGRATION TESTS ====================
print(f"\n{BLUE}{'=' * 60}{RESET}")
print(f"{BLUE}INTEGRATION TESTS{RESET}")
print(f"{BLUE}{'=' * 60}{RESET}\n")


def test_complete_place_setup():
    """Test complete place setup with owner and amenities"""
    # Create owner
    owner = UserModel(first_name="John", last_name="Owner",
                      email="john.owner@example.com")

    # Create place
    place = PlaceModel(
        title="Beach House",
        description="Beautiful beach house with ocean view",
        price=250,
        latitude=25.7617,
        longitude=-80.1918,
        owner=owner
    )

    # Create and add amenities
    amenities = [
        AmenityModel(name="Wi-Fi"),
        AmenityModel(name="Ocean View"),
        AmenityModel(name="BBQ Grill"),
        AmenityModel(name="Beach Access")
    ]

    for amenity in amenities:
        place.add_amenity(amenity)

    # Assertions
    assert (place.owner.email == "john.owner@example.com",
            "Owner email should match")
    assert len(place.amenities) == 4, "Should have 4 amenities"
    assert place.price == 250, "Price should be 250"
    assert "Beach" in place.title, "Title should contain 'Beach'"


run_test("Complete place setup integration", test_complete_place_setup)


def test_multiple_places_same_owner():
    """Test one owner with multiple places"""
    owner = UserModel(first_name="Multi", last_name="Owner",
                      email="multi@example.com")

    places = [
        PlaceModel(
            title="Apartment 1",
            price=100,
            latitude=0,
            longitude=0,
            owner=owner),
        PlaceModel(
            title="Apartment 2",
            price=150,
            latitude=1,
            longitude=1,
            owner=owner),
        PlaceModel(
            title="Villa",
            price=500,
            latitude=2,
            longitude=2,
            owner=owner)]

    for place in places:
        assert place.owner == owner, "All places should have same owner"

    assert len(places) == 3, "Should have 3 places"
    assert all(p.owner.email == "multi@example.com" for p in places), \
        "All should link to same owner"


run_test("Multiple places same owner", test_multiple_places_same_owner)


def test_shared_amenities():
    """Test multiple places sharing amenities"""
    owner = UserModel(first_name="Owner", last_name="Test",
                      email="owner@example.com")

    wifi = AmenityModel(name="Wi-Fi")
    parking = AmenityModel(name="Parking")

    place1 = PlaceModel(
        title="Place 1",
        price=100,
        latitude=0,
        longitude=0,
        owner=owner)
    place2 = PlaceModel(
        title="Place 2",
        price=200,
        latitude=1,
        longitude=1,
        owner=owner)

    place1.add_amenity(wifi)
    place1.add_amenity(parking)
    place2.add_amenity(wifi)
    place2.add_amenity(parking)

    assert (wifi in place1.amenities and wifi in place2.amenities), \
        "Wi-Fi should be in both places"
    assert (parking in place1.amenities and parking in place2.amenities), \
        "Parking should be in both places"


run_test("Shared amenities across places", test_shared_amenities)

# ==================== TEST SUMMARY ====================
print(f"\n{BLUE}{'=' * 60}{RESET}")
print(f"{BLUE}TEST SUMMARY{RESET}")
print(f"{BLUE}{'=' * 60}{RESET}\n")

total_tests = test_results["passed"] + test_results["failed"]
success_rate = (
    test_results["passed"] /
    total_tests *
    100) if total_tests > 0 else 0

print(f"Total tests run: {total_tests}")
print(f"{GREEN}Passed: {test_results['passed']}{RESET}")
print(f"{RED}Failed: {test_results['failed']}{RESET}")
print(f"Success rate: {success_rate:.1f}%")

if test_results["failed"] == 0:
    print(f"{GREEN}🎉 All tests passed!{RESET}\n")
else:
    print(f"{YELLOW}⚠ Some tests failed. Please review the output above."
          f"{RESET}\n")
