import unittest
from app import create_app


class TestEndpointsValidation(unittest.TestCase):
    """
    Validation tests for all HBNB API endpoints

    Validation tests implemented:
    - User: first_name, last_name, email (not empty + valid email format)
    - Place: title (not empty), price (positive), latitude (-90 to 90),
      longitude (-180 to 180)
    - Review: text (not empty), user_id and place_id (valid entities)
    """

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    # ========================================================================
    # USER TESTS - Attribute validation
    # ========================================================================

    def test_create_user_valid_data(self):
        """Test creating user with valid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'jane.doe@example.com')

    def test_create_user_empty_first_name(self):
        """Test creating user with empty first_name"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_create_user_empty_last_name(self):
        """Test creating user with empty last_name"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_create_user_empty_email(self):
        """Test creating user with empty email"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_create_user_invalid_email_format(self):
        """Test creating user with invalid email format"""
        invalid_emails = [
            "invalid-email",
            "user@",
            "@domain.com",
            "user.domain.com",
            "user @domain.com",
            "user@domain",
            "user@.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                response = self.client.post('/api/v1/users/', json={
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": email
                })
                self.assertEqual(response.status_code, 400)
                data = response.get_json()
                self.assertIn('message', data)

    def test_create_user_missing_required_fields(self):
        """Test creating user with missing required fields"""
        # Test without first_name
        response = self.client.post('/api/v1/users/', json={
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

        # Test without last_name
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

        # Test without email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_whitespace_only_fields(self):
        """Test creating user with fields containing only whitespace"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "   ",
            "last_name": "   ",
            "email": "janette.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test creating user with duplicate email returns 409"""
        # Create first user
        response1 = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        self.assertEqual(response1.status_code, 201)

        # Try to create user with same email
        response2 = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "duplicate@example.com"
        })
        self.assertEqual(response2.status_code, 409)
        data = response2.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Email already registered')

    # ========================================================================
    # PLACE TESTS - Attribute validation
    # ========================================================================

    def test_create_place_valid_data(self):
        """Test creating place with valid data"""
        # Create owner user first
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@example.com"
        })
        self.assertEqual(user_response.status_code, 201)
        owner_id = user_response.get_json()['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Beach House",
            "description": "A lovely house by the beach",
            "price": 150.0,
            "latitude": 25.7617,
            "longitude": -80.1918,
            "owner_id": owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Beach House')

    def test_create_place_empty_title(self):
        """Test creating place with empty title"""
        # Create owner user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner2@example.com"
        })
        owner_id = user_response.get_json()['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "Description",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        """Test creating place with negative price"""
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner3@example.com"
        })
        owner_id = user_response.get_json()['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Description",
            "price": -50.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_zero_price(self):
        """Test creating place with zero price"""
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner4@example.com"
        })
        owner_id = user_response.get_json()['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Description",
            "price": 0.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test creating place with invalid latitude"""
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner5@example.com"
        })
        owner_id = user_response.get_json()['id']

        invalid_latitudes = [-91.0, 91.0, -100.0, 200.0]

        for latitude in invalid_latitudes:
            with self.subTest(latitude=latitude):
                response = self.client.post('/api/v1/places/', json={
                    "title": "Test Place",
                    "description": "Description",
                    "price": 100.0,
                    "latitude": latitude,
                    "longitude": -80.0,
                    "owner_id": owner_id
                })
                self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test creating place with invalid longitude"""
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner6@example.com"
        })
        owner_id = user_response.get_json()['id']

        invalid_longitudes = [-181.0, 181.0, -200.0, 300.0]

        for longitude in invalid_longitudes:
            with self.subTest(longitude=longitude):
                response = self.client.post('/api/v1/places/', json={
                    "title": "Test Place",
                    "description": "Description",
                    "price": 100.0,
                    "latitude": 25.0,
                    "longitude": longitude,
                    "owner_id": owner_id
                })
                self.assertEqual(response.status_code, 400)

    def test_create_place_valid_boundary_coordinates(self):
        """Test creating place with valid boundary coordinates"""
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner7@example.com"
        })
        owner_id = user_response.get_json()['id']

        # Test valid boundaries
        valid_coordinates = [
            {"latitude": -90.0, "longitude": -180.0},  # Min boundaries
            {"latitude": 90.0, "longitude": 180.0},    # Max boundaries
            {"latitude": 0.0, "longitude": 0.0}        # Center
        ]

        for i, coords in enumerate(valid_coordinates):
            with self.subTest(coords=coords):
                response = self.client.post('/api/v1/places/', json={
                    "title": f"Boundary Test Place {i}",
                    "description": "Description",
                    "price": 100.0,
                    "latitude": coords["latitude"],
                    "longitude": coords["longitude"],
                    "owner_id": owner_id
                })
                self.assertEqual(response.status_code, 201)

    # ========================================================================
    # REVIEW TESTS - Attribute validation
    # ========================================================================

    def test_create_review_valid_data(self):
        """Test creating review with valid data"""
        # Create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer@example.com"
        })
        user_id = user_response.get_json()['id']

        # Create owner
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "placeowner@example.com"
        })
        owner_id = owner_response.get_json()['id']

        # Create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Test Place",
            "description": "Place for review testing",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        place_id = place_response.get_json()['id']

        # Create review
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place to stay!')

    def test_create_review_empty_text(self):
        """Test creating review with empty text"""
        # Create prerequisites
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer2@example.com"
        })
        user_id = user_response.get_json()['id']

        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "placeowner2@example.com"
        })
        owner_id = owner_response.get_json()['id']

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Test Place 2",
            "description": "Place for review testing",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        place_id = place_response.get_json()['id']

        # Test with empty text
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_whitespace_only_text(self):
        """Test creating review with text containing only whitespace"""
        # Create prerequisites
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer3@example.com"
        })
        user_id = user_response.get_json()['id']

        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "placeowner3@example.com"
        })
        owner_id = owner_response.get_json()['id']

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Test Place 3",
            "description": "Place for review testing",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        place_id = place_response.get_json()['id']

        # Test with whitespace only
        response = self.client.post('/api/v1/reviews/', json={
            "text": "   ",
            "rating": 4,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user_id(self):
        """Test creating review with invalid user_id"""
        # Create place only
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "placeowner4@example.com"
        })
        owner_id = owner_response.get_json()['id']

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Test Place 4",
            "description": "Place for review testing",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        place_id = place_response.get_json()['id']

        # Test with non-existent user_id
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 4,
            "user_id": "12345678-1234-1234-1234-123456789012",
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_place_id(self):
        """Test creating review with invalid place_id"""
        # Create user only
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer5@example.com"
        })
        user_id = user_response.get_json()['id']

        # Test with non-existent place_id
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 4,
            "user_id": user_id,
            "place_id": "12345678-1234-1234-1234-123456789012"
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_rating(self):
        """Test creating review with invalid rating"""
        # Create prerequisites
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer6@example.com"
        })
        user_id = user_response.get_json()['id']

        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "placeowner6@example.com"
        })
        owner_id = owner_response.get_json()['id']

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Test Place 6",
            "description": "Place for review testing",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0,
            "owner_id": owner_id
        })
        place_id = place_response.get_json()['id']

        # Test invalid ratings
        invalid_ratings = [0, 6, -1, 10]

        for rating in invalid_ratings:
            with self.subTest(rating=rating):
                response = self.client.post('/api/v1/reviews/', json={
                    "text": "Test review",
                    "rating": rating,
                    "user_id": user_id,
                    "place_id": place_id
                })
                self.assertEqual(response.status_code, 400)

    # ========================================================================
    # AMENITY TESTS - Attribute validation
    # ========================================================================

    def test_create_amenity_valid_data(self):
        """Test creating amenity with valid data"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_empty_text(self):
        """Test creating amenity with empty name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_amenity_whitespace_only_text(self):
        """Test creating amenity with whitespace-only name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "   "
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_amenity_already_exist(self):
        """Test creating duplicate amenity"""
        # Create first amenity
        response1 = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response1.status_code, 201)

        # Try to create duplicate
        response2 = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response2.status_code, 400)
        data = response2.get_json()
        self.assertIn('error', data)

    def test_create_amenity_missing_name(self):
        """Test creating amenity without name field"""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_amenity_name_too_long(self):
        """Test creating amenity with name exceeding maximum length"""
        long_name = "A" * 51  # Exceeds 50 character limit
        response = self.client.post('/api/v1/amenities/', json={
            "name": long_name
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
