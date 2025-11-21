"""
Unit tests for core model classes (independent tests)
Tests the business logic and validation rules without API layer
"""
import unittest
from datetime import datetime, timezone
from app import create_app, db
from app.models.user import UserModel
from app.models.amenity import AmenityModel
from app.models.place import PlaceModel
from app.models.review import ReviewModel


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test fixtures"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_base_model_id_generation(self):
        """Test that BaseModel generates unique IDs"""
        user1 = UserModel(
            first_name="John",
            last_name="Doe",
            email="john1@example.com",
            password="password123"
        )
        user2 = UserModel(
            first_name="Jane",
            last_name="Doe",
            email="jane2@example.com",
            password="password123"
        )
        
        self.assertIsNotNone(user1.id)
        self.assertIsNotNone(user2.id)
        self.assertNotEqual(user1.id, user2.id)
        print("✓ BaseModel generates unique IDs")

    def test_base_model_timestamps(self):
        """Test that BaseModel creates timestamps"""
        user = UserModel(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()
        
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
        print("✓ BaseModel creates timestamps correctly")

    def test_base_model_save_updates_timestamp(self):
        """Test that save() updates the updated_at timestamp"""
        user = UserModel(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()
        
        original_updated_at = user.updated_at
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp difference
        
        user.save()
        db.session.commit()
        # Compare timestamps as strings to avoid timezone issues
        self.assertNotEqual(str(user.updated_at), str(original_updated_at))
        print("✓ BaseModel.save() updates timestamp")


class TestUserModel(unittest.TestCase):
    """Test the UserModel class"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test fixtures"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation_valid(self):
        """Test creating a user with valid data"""
        user = UserModel(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)
        print("✓ User created with valid data")

    def test_user_first_name_validation_empty(self):
        """Test first_name validation with empty string"""
        with self.assertRaises(ValueError) as context:
            user = UserModel(
                first_name="",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
        self.assertIn("First name is required", str(context.exception))
        print("✓ User validates empty first_name")

    def test_user_first_name_validation_whitespace(self):
        """Test first_name validation with whitespace only"""
        with self.assertRaises(ValueError) as context:
            user = UserModel(
                first_name="   ",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
        self.assertIn("First name is required", str(context.exception))
        print("✓ User validates whitespace-only first_name")

    def test_user_first_name_validation_too_long(self):
        """Test first_name validation with too long string"""
        with self.assertRaises(ValueError) as context:
            user = UserModel(
                first_name="a" * 51,
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
        self.assertIn("must be <= 50 chars", str(context.exception))
        print("✓ User validates first_name length")

    def test_user_last_name_validation_empty(self):
        """Test last_name validation with empty string"""
        with self.assertRaises(ValueError) as context:
            user = UserModel(
                first_name="John",
                last_name="",
                email="john@example.com",
                password="password123"
            )
        self.assertIn("Last name is required", str(context.exception))
        print("✓ User validates empty last_name")

    def test_user_email_validation_invalid(self):
        """Test email validation with invalid format"""
        with self.assertRaises(ValueError) as context:
            user = UserModel(
                first_name="John",
                last_name="Doe",
                email="invalid-email",
                password="password123"
            )
        self.assertIn("Valid email is required", str(context.exception))
        print("✓ User validates email format")

    def test_user_email_validation_missing_at(self):
        """Test email validation missing @ symbol"""
        with self.assertRaises(ValueError) as context:
            user = UserModel(
                first_name="John",
                last_name="Doe",
                email="johndoe.com",
                password="password123"
            )
        self.assertIn("Valid email is required", str(context.exception))
        print("✓ User validates email @ symbol")

    def test_user_password_hashing(self):
        """Test password hashing functionality"""
        user = UserModel(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123"
        )
        plain_password = "mySecretPassword"
        user.hash_password(plain_password)
        
        self.assertNotEqual(user.password, plain_password)
        self.assertTrue(user.verify_password(plain_password))
        self.assertFalse(user.verify_password("wrongPassword"))
        print("✓ User password hashing works correctly")

    def test_user_is_admin_default(self):
        """Test that is_admin defaults to False"""
        user = UserModel(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123"
        )
        self.assertFalse(user.is_admin)
        print("✓ User is_admin defaults to False")


class TestAmenityModel(unittest.TestCase):
    """Test the AmenityModel class"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test fixtures"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_amenity_creation_valid(self):
        """Test creating an amenity with valid data"""
        amenity = AmenityModel(name="WiFi")
        db.session.add(amenity)
        db.session.commit()
        
        self.assertEqual(amenity.name, "WiFi")
        self.assertIsNotNone(amenity.id)
        print("✓ Amenity created with valid data")

    def test_amenity_name_validation_empty(self):
        """Test name validation with empty string"""
        with self.assertRaises(ValueError) as context:
            amenity = AmenityModel(name="")
        # The validator checks for empty string and raises this message
        self.assertIn("Name is required", str(context.exception))
        print("✓ Amenity validates empty name")

    def test_amenity_name_validation_whitespace(self):
        """Test name validation with whitespace only"""
        with self.assertRaises(ValueError) as context:
            amenity = AmenityModel(name="   ")
        self.assertIn("Name cannot be empty", str(context.exception))
        print("✓ Amenity validates whitespace-only name")

    def test_amenity_name_validation_too_long(self):
        """Test name validation with too long string"""
        with self.assertRaises(ValueError) as context:
            amenity = AmenityModel(name="a" * 51)
        self.assertIn("must not exceed 50 characters", str(context.exception))
        print("✓ Amenity validates name length")

    def test_amenity_name_validation_not_string(self):
        """Test name validation with non-string type"""
        with self.assertRaises(ValueError) as context:
            amenity = AmenityModel(name=123)
        self.assertIn("must be a string", str(context.exception))
        print("✓ Amenity validates name type")

    def test_amenity_update(self):
        """Test amenity update method"""
        amenity = AmenityModel(name="WiFi")
        db.session.add(amenity)
        db.session.commit()
        
        original_updated_at = amenity.updated_at
        import time
        time.sleep(0.1)
        
        amenity.update({'name': 'WiFi Pro'})
        db.session.commit()
        self.assertEqual(amenity.name, "WiFi Pro")
        # Compare as strings to avoid timezone issues
        self.assertNotEqual(str(amenity.updated_at), str(original_updated_at))
        print("✓ Amenity update works correctly")


class TestPlaceModel(unittest.TestCase):
    """Test the PlaceModel class"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create a test user for place ownership
        self.user = UserModel(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down test fixtures"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_place_creation_valid(self):
        """Test creating a place with valid data"""
        place = PlaceModel(
            title="Beautiful Apartment",
            description="A nice place to stay",  # description is required
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(place)
        db.session.commit()
        
        self.assertEqual(place.title, "Beautiful Apartment")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        print("✓ Place created with valid data")

    def test_place_title_validation_empty(self):
        """Test title validation with empty string"""
        with self.assertRaises(ValueError) as context:
            place = PlaceModel(
                title="",
                description="Test",
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=self.user.id
            )
        self.assertIn("Required", str(context.exception))
        print("✓ Place validates empty title")

    def test_place_price_validation_negative(self):
        """Test price validation with negative value"""
        with self.assertRaises(ValueError) as context:
            place = PlaceModel(
                title="Test Place",
                description="Test",
                price=-50.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=self.user.id
            )
        self.assertIn("price must be positive", str(context.exception))
        print("✓ Place validates negative price")

    def test_place_latitude_validation_out_of_range(self):
        """Test latitude validation with out of range value"""
        with self.assertRaises(ValueError) as context:
            place = PlaceModel(
                title="Test Place",
                description="Test",
                price=100.0,
                latitude=95.0,
                longitude=-74.0060,
                owner_id=self.user.id
            )
        self.assertIn("latitude must be between -90.0 and 90.0", str(context.exception))
        print("✓ Place validates latitude range")

    def test_place_longitude_validation_out_of_range(self):
        """Test longitude validation with out of range value"""
        with self.assertRaises(ValueError) as context:
            place = PlaceModel(
                title="Test Place",
                description="Test",
                price=100.0,
                latitude=40.7128,
                longitude=190.0,
                owner_id=self.user.id
            )
        self.assertIn("longitude must be between -180.0 and 180.0", str(context.exception))
        print("✓ Place validates longitude range")


class TestReviewModel(unittest.TestCase):
    """Test the ReviewModel class"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user and place with unique email for each test
        import uuid
        self.user = UserModel(
            first_name="John",
            last_name="Doe",
            email=f"john-{uuid.uuid4().hex[:8]}@example.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()
        
        self.place = PlaceModel(
            title="Test Place",
            description="A test place",  # description is required
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(self.place)
        db.session.commit()

    def tearDown(self):
        """Tear down test fixtures"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_review_creation_valid(self):
        """Test creating a review with valid data"""
        review = ReviewModel(
            text="Great place!",
            rating=5,
            place_id=self.place.id,
            user_id=self.user.id
        )
        db.session.add(review)
        db.session.commit()
        
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        print("✓ Review created with valid data")

    def test_review_text_validation_empty(self):
        """Test text validation with empty string"""
        with self.assertRaises(ValueError) as context:
            review = ReviewModel(
                text="",
                rating=5,
                place_id=self.place.id,
                user_id=self.user.id
            )
        self.assertIn("cannot be empty", str(context.exception))
        print("✓ Review validates empty text")

    def test_review_rating_validation_below_range(self):
        """Test rating validation below valid range"""
        with self.assertRaises(ValueError) as context:
            review = ReviewModel(
                text="Test review",
                rating=0,
                place_id=self.place.id,
                user_id=self.user.id
            )
        self.assertIn("between 1 and 5", str(context.exception))
        print("✓ Review validates rating minimum")

    def test_review_rating_validation_above_range(self):
        """Test rating validation above valid range"""
        with self.assertRaises(ValueError) as context:
            review = ReviewModel(
                text="Test review",
                rating=6,
                place_id=self.place.id,
                user_id=self.user.id
            )
        self.assertIn("between 1 and 5", str(context.exception))
        print("✓ Review validates rating maximum")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
