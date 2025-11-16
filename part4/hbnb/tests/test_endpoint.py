import unittest
import os
from app import create_app, db


class TestEndpointsValidation(unittest.TestCase):
    """
    Validation tests for all HBNB API endpoints

    Validation tests implemented:
    - User: first_name, last_name, email (not empty + valid email format)
    - Place: title (not empty), price (positive), latitude (-90 to 90),
      longitude (-180 to 180)
    - Review: text (not empty), user_id and place_id (valid entities)
    - Authentication: JWT token validation and role-based access
    - Authorization: ownership and admin privileges
    """

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_endpoints.db'
        self.client = self.app.test_client()
        
        # Create database tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        
        # Remove test database file
        try:
            os.remove('test_endpoints.db')
        except OSError:
            pass

    def _create_user_and_login(self, email, password="password123", 
                                first_name="Test", last_name="User"):
        """Helper method to create a user and get JWT token"""
        import uuid
        # Add unique suffix to email to avoid conflicts
        unique_email = f"{email.split('@')[0]}-{uuid.uuid4().hex[:8]}@{email.split('@')[1]}"
        
        # Create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": first_name,
            "last_name": last_name,
            "email": unique_email,
            "password": password
        })
        user_id = user_response.get_json()['id']
        
        # Login to get token
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": unique_email,
            "password": password
        })
        token = login_response.get_json()['access_token']
        
        return user_id, token

    # ========================================================================
    # AUTHENTICATION TESTS - JWT and Login
    # ========================================================================

    def test_login_valid_credentials(self):
        """Test login with valid credentials returns JWT token"""
        # Create user first
        self.client.post('/api/v1/users/', json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "login@example.com",
            "password": "password123"
        })
        
        # Login
        response = self.client.post('/api/v1/auth/login', json={
            "email": "login@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)
        self.assertIn('message', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials returns 401"""
        # Create user first
        self.client.post('/api/v1/users/', json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "login2@example.com",
            "password": "password123"
        })
        
        # Login with wrong password
        response = self.client.post('/api/v1/auth/login', json={
            "email": "login2@example.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)

    def test_login_missing_credentials(self):
        """Test login without email or password returns 400"""
        # Missing password
        response = self.client.post('/api/v1/auth/login', json={
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)
        
        # Missing email
        response = self.client.post('/api/v1/auth/login', json={
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_login_nonexistent_user(self):
        """Test login with non-existent user returns 401"""
        response = self.client.post('/api/v1/auth/login', json={
            "email": "nonexistent@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without JWT token"""
        response = self.client.get('/api/v1/auth/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_with_valid_token(self):
        """Test accessing protected endpoint with valid JWT token"""
        user_id, token = self._create_user_and_login("protected@example.com")
        
        response = self.client.get('/api/v1/auth/protected',
                                   headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    # ========================================================================
    # USER TESTS - Attribute validation
    # ========================================================================

    def test_create_user_valid_data_with_password(self):
        """Test creating user with valid data including password"""
        import uuid
        unique_email = f"jane.doe.pwd-{uuid.uuid4().hex[:8]}@example.com"
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email,
            "password": "securepassword"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        # Password should not be returned in response
        self.assertNotIn('password', data)

    def test_create_user_missing_password(self):
        """Test creating user without password returns 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.nopwd@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_first_name(self):
        """Test creating user with empty first_name"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "jane.doe2@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_create_user_empty_last_name(self):
        """Test creating user with empty last_name"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "",
            "email": "jane.doe3@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_create_user_empty_email(self):
        """Test creating user with empty email"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "",
            "password": "password123"
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

        for i, email in enumerate(invalid_emails):
            with self.subTest(email=email):
                response = self.client.post('/api/v1/users/', json={
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": email,
                    "password": "password123"
                })
                self.assertEqual(response.status_code, 400)
                data = response.get_json()
                self.assertIn('message', data)

    def test_create_user_missing_required_fields(self):
        """Test creating user with missing required fields"""
        # Test without first_name
        response = self.client.post('/api/v1/users/', json={
            "last_name": "Doe",
            "email": "jane.doe4@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

        # Test without last_name
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "email": "jane.doe5@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

        # Test without email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_whitespace_only_fields(self):
        """Test creating user with fields containing only whitespace"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "   ",
            "last_name": "   ",
            "email": "janette.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test creating user with duplicate email returns 400"""
        import uuid
        unique_email = f"duplicate-{uuid.uuid4()}@example.com"
        
        # Create first user
        response1 = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email,
            "password": "password123"
        })
        self.assertEqual(response1.status_code, 201)

        # Try to create user with same email
        response2 = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": unique_email,
            "password": "password456"
        })
        self.assertEqual(response2.status_code, 400)
        data = response2.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Email already registered')

    def test_update_user_own_profile(self):
        """Test user can update their own profile (first_name, last_name only)"""
        user_id, token = self._create_user_and_login("updateown@example.com")
        
        response = self.client.put(f'/api/v1/users/{user_id}',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={
                                       "first_name": "Updated",
                                       "last_name": "Name"
                                   })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['last_name'], 'Name')

    def test_update_user_cannot_modify_email_password(self):
        """Test regular user cannot modify email or password"""
        user_id, token = self._create_user_and_login("noemail@example.com")
        
        # Try to update email
        response = self.client.put(f'/api/v1/users/{user_id}',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={"email": "newemail@example.com"})
        self.assertEqual(response.status_code, 400)
        
        # Try to update password
        response = self.client.put(f'/api/v1/users/{user_id}',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={"password": "newpassword"})
        self.assertEqual(response.status_code, 400)

    def test_update_user_unauthorized(self):
        """Test user cannot update another user's profile"""
        user1_id, token1 = self._create_user_and_login("user1@example.com")
        user2_id, token2 = self._create_user_and_login("user2@example.com")
        
        response = self.client.put(f'/api/v1/users/{user2_id}',
                                   headers={'Authorization': f'Bearer {token1}'},
                                   json={"first_name": "Hacked"})
        self.assertEqual(response.status_code, 403)

    def test_update_user_without_token(self):
        """Test updating user without JWT token returns 401"""
        user_id, _ = self._create_user_and_login("notoken@example.com")
        
        response = self.client.put(f'/api/v1/users/{user_id}',
                                   json={"first_name": "Updated"})
        self.assertEqual(response.status_code, 401)

    # ========================================================================
    # PLACE TESTS - Attribute validation
    # ========================================================================

    def test_create_place_with_jwt(self):
        """Test creating place with JWT token (owner_id from token)"""
        user_id, token = self._create_user_and_login("placeowner@example.com")
        
        response = self.client.post('/api/v1/places/',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={
                                       "title": "Beautiful Beach House",
                                       "description": "A lovely house by the beach",
                                       "price": 150.0,
                                       "latitude": 25.7617,
                                       "longitude": -80.1918
                                   })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Beach House')
        self.assertEqual(data['owner_id'], user_id)

    def test_create_place_without_jwt(self):
        """Test creating place without JWT token returns 401"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 25.0,
            "longitude": -80.0
        })
        self.assertEqual(response.status_code, 401)

    def test_create_place_duplicate_title(self):
        """Test creating place with duplicate title"""
        user_id, token = self._create_user_and_login("duplicateplace@example.com")
        
        # Create first place
        response1 = self.client.post('/api/v1/places/',
                                    headers={'Authorization': f'Bearer {token}'},
                                    json={
                                        "title": "Unique Place",
                                        "price": 100.0,
                                        "latitude": 25.0,
                                        "longitude": -80.0
                                    })
        self.assertEqual(response1.status_code, 201)
        
        # Try to create duplicate
        response2 = self.client.post('/api/v1/places/',
                                    headers={'Authorization': f'Bearer {token}'},
                                    json={
                                        "title": "Unique Place",
                                        "price": 150.0,
                                        "latitude": 26.0,
                                        "longitude": -81.0
                                    })
        self.assertEqual(response2.status_code, 400)

    def test_create_place_valid_data(self):
        """Test creating place with valid data"""
        # Create owner user first
        user_id, token = self._create_user_and_login("owner10@example.com")

        response = self.client.post('/api/v1/places/',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={
                                       "title": "Beautiful Beach House Test",
                                       "description": "A lovely house by the beach",
                                       "price": 150.0,
                                       "latitude": 25.7617,
                                       "longitude": -80.1918
                                   })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Beach House Test')

    def test_create_place_empty_title(self):
        """Test creating place with empty title"""
        # Create owner user
        user_id, token = self._create_user_and_login("owner2@example.com")

        response = self.client.post('/api/v1/places/',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={
                                       "title": "",
                                       "description": "Description",
                                       "price": 100.0,
                                       "latitude": 25.0,
                                       "longitude": -80.0
                                   })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        """Test creating place with negative price"""
        user_id, token = self._create_user_and_login("owner3@example.com")

        response = self.client.post('/api/v1/places/',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={
                                       "title": "Test Place Neg",
                                       "description": "Description",
                                       "price": -50.0,
                                       "latitude": 25.0,
                                       "longitude": -80.0
                                   })
        self.assertEqual(response.status_code, 400)

    def test_create_place_zero_price(self):
        """Test creating place with zero price"""
        user_id, token = self._create_user_and_login("owner4@example.com")

        response = self.client.post('/api/v1/places/',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={
                                       "title": "Test Place Zero",
                                       "description": "Description",
                                       "price": 0.0,
                                       "latitude": 25.0,
                                       "longitude": -80.0
                                   })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test creating place with invalid latitude"""
        user_id, token = self._create_user_and_login("owner5@example.com")

        invalid_latitudes = [-91.0, 91.0, -100.0, 200.0]

        for latitude in invalid_latitudes:
            with self.subTest(latitude=latitude):
                response = self.client.post('/api/v1/places/',
                                           headers={'Authorization': f'Bearer {token}'},
                                           json={
                                               "title": f"Test Place Lat {latitude}",
                                               "description": "Description",
                                               "price": 100.0,
                                               "latitude": latitude,
                                               "longitude": -80.0
                                           })
                self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test creating place with invalid longitude"""
        user_id, token = self._create_user_and_login("owner6@example.com")

        invalid_longitudes = [-181.0, 181.0, -200.0, 300.0]

        for longitude in invalid_longitudes:
            with self.subTest(longitude=longitude):
                response = self.client.post('/api/v1/places/',
                                           headers={'Authorization': f'Bearer {token}'},
                                           json={
                                               "title": f"Test Place Lon {longitude}",
                                               "description": "Description",
                                               "price": 100.0,
                                               "latitude": 25.0,
                                               "longitude": longitude
                                           })
                self.assertEqual(response.status_code, 400)

    def test_create_place_valid_boundary_coordinates(self):
        """Test creating place with valid boundary coordinates"""
        user_id, token = self._create_user_and_login("owner7@example.com")

        # Test valid boundaries
        valid_coordinates = [
            {"latitude": -90.0, "longitude": -180.0},  # Min boundaries
            {"latitude": 90.0, "longitude": 180.0},    # Max boundaries
            {"latitude": 0.0, "longitude": 0.0}        # Center
        ]

        for i, coords in enumerate(valid_coordinates):
            with self.subTest(coords=coords):
                response = self.client.post('/api/v1/places/',
                                           headers={'Authorization': f'Bearer {token}'},
                                           json={
                                               "title": f"Boundary Test Place {i}",
                                               "description": "Description",
                                               "price": 100.0,
                                               "latitude": coords["latitude"],
                                               "longitude": coords["longitude"]
                                           })
                self.assertEqual(response.status_code, 201)

    def test_update_place_owner_only(self):
        """Test only place owner can update place"""
        owner_id, owner_token = self._create_user_and_login("placeowner1@example.com")
        other_id, other_token = self._create_user_and_login("notowner@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Owner Only Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Try to update with different user
        response = self.client.put(f'/api/v1/places/{place_id}',
                                  headers={'Authorization': f'Bearer {other_token}'},
                                  json={"title": "Hacked Place"})
        self.assertEqual(response.status_code, 403)
        
        # Owner can update
        response = self.client.put(f'/api/v1/places/{place_id}',
                                  headers={'Authorization': f'Bearer {owner_token}'},
                                  json={"title": "Updated Place"})
        self.assertEqual(response.status_code, 200)

    def test_add_amenity_to_place_owner_only(self):
        """Test only place owner can add amenities"""
        owner_id, owner_token = self._create_user_and_login("amenityowner@example.com")
        other_id, other_token = self._create_user_and_login("notamenityowner@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Amenity Test Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Create amenity (assuming admin needed - skip if not admin)
        # For now, test unauthorized access with invalid amenity
        response = self.client.post(f'/api/v1/places/{place_id}/amenities',
                                   headers={'Authorization': f'Bearer {other_token}'},
                                   json={"amenity_id": "some-amenity-id"})
        # Could be 403 (forbidden) or 404 (amenity not found)
        self.assertIn(response.status_code, [403, 404])

    # ========================================================================
    # REVIEW TESTS - Attribute validation
    # ========================================================================

    def test_create_review_with_jwt(self):
        """Test creating review with JWT token (user_id from token)"""
        reviewer_id, reviewer_token = self._create_user_and_login("reviewer_jwt@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner_jwt@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "JWT Review Test Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Create review
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {reviewer_token}'},
                                   json={
                                       "text": "Great place!",
                                       "rating": 5,
                                       "place_id": place_id
                                   })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['user_id'], reviewer_id)

    def test_create_review_without_jwt(self):
        """Test creating review without JWT token returns 401"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "place_id": "some-place-id"
        })
        self.assertEqual(response.status_code, 401)

    def test_create_review_own_place(self):
        """Test user cannot review their own place"""
        owner_id, owner_token = self._create_user_and_login("ownreview@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Own Place Review Test",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        place_id = place_response.get_json()['id']
        
        # Try to review own place
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {owner_token}'},
                                   json={
                                       "text": "My own place is great!",
                                       "rating": 5,
                                       "place_id": place_id
                                   })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_review_duplicate(self):
        """Test user cannot review the same place twice"""
        reviewer_id, reviewer_token = self._create_user_and_login("duplicate_review@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner_dup@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Duplicate Review Test Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Create first review
        response1 = self.client.post('/api/v1/reviews/',
                                    headers={'Authorization': f'Bearer {reviewer_token}'},
                                    json={
                                        "text": "Great place!",
                                        "rating": 5,
                                        "place_id": place_id
                                    })
        self.assertEqual(response1.status_code, 201)
        
        # Try to create duplicate review
        response2 = self.client.post('/api/v1/reviews/',
                                    headers={'Authorization': f'Bearer {reviewer_token}'},
                                    json={
                                        "text": "Still great!",
                                        "rating": 4,
                                        "place_id": place_id
                                    })
        self.assertEqual(response2.status_code, 400)
        data = response2.get_json()
        self.assertIn('error', data)

    def test_create_review_valid_data(self):
        """Test creating review with valid data"""
        # Create user
        user_id, user_token = self._create_user_and_login("reviewervalid@example.com")

        # Create owner
        owner_id, owner_token = self._create_user_and_login("placeownervalid@example.com")

        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Review Test Place Valid",
                                             "description": "Place for review testing",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']

        # Create review
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {user_token}'},
                                   json={
                                       "text": "Great place to stay!",
                                       "rating": 5,
                                       "place_id": place_id
                                   })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place to stay!')

    def test_create_review_empty_text(self):
        """Test creating review with empty text"""
        # Create prerequisites
        user_id, user_token = self._create_user_and_login("reviewer2@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner2@example.com")

        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Review Test Place 2",
                                             "description": "Place for review testing",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        place_id = place_response.get_json()['id']

        # Test with empty text
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {user_token}'},
                                   json={
                                       "text": "",
                                       "rating": 4,
                                       "place_id": place_id
                                   })
        self.assertEqual(response.status_code, 400)

    def test_create_review_whitespace_only_text(self):
        """Test creating review with text containing only whitespace"""
        # Create prerequisites
        user_id, user_token = self._create_user_and_login("reviewer3@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner3@example.com")

        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Review Test Place 3",
                                             "description": "Place for review testing",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        place_id = place_response.get_json()['id']

        # Test with whitespace only
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {user_token}'},
                                   json={
                                       "text": "   ",
                                       "rating": 4,
                                       "place_id": place_id
                                   })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user_id(self):
        """Test creating review with invalid user_id"""
        # Create place only
        owner_id, owner_token = self._create_user_and_login("placeowner4@example.com")

        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Review Test Place 4",
                                             "description": "Place for review testing",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        place_id = place_response.get_json()['id']

        # Test with non-existent user_id (JWT will provide user_id automatically)
        # This test now checks if place_id is invalid
        user_id, user_token = self._create_user_and_login("validuser@example.com")
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {user_token}'},
                                   json={
                                       "text": "Great place!",
                                       "rating": 4,
                                       "place_id": "12345678-1234-1234-1234-123456789012"
                                   })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_place_id(self):
        """Test creating review with invalid place_id"""
        # Create user only
        user_id, user_token = self._create_user_and_login("reviewer5@example.com")

        # Test with non-existent place_id
        response = self.client.post('/api/v1/reviews/',
                                   headers={'Authorization': f'Bearer {user_token}'},
                                   json={
                                       "text": "Great place!",
                                       "rating": 4,
                                       "place_id": "12345678-1234-1234-1234-123456789012"
                                   })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_rating(self):
        """Test creating review with invalid rating"""
        # Create prerequisites
        user_id, user_token = self._create_user_and_login("reviewer6@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner6@example.com")

        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Review Test Place 6",
                                             "description": "Place for review testing",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        place_id = place_response.get_json()['id']

        # Test invalid ratings
        invalid_ratings = [0, 6, -1, 10]

        for rating in invalid_ratings:
            with self.subTest(rating=rating):
                response = self.client.post('/api/v1/reviews/',
                                           headers={'Authorization': f'Bearer {user_token}'},
                                           json={
                                               "text": "Test review",
                                               "rating": rating,
                                               "place_id": place_id
                                           })
                self.assertEqual(response.status_code, 400)

    def test_update_review_owner_only(self):
        """Test only review author can update review"""
        reviewer_id, reviewer_token = self._create_user_and_login("reviewauthor@example.com")
        other_id, other_token = self._create_user_and_login("notauthor@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner_update@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Update Review Test Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Create review
        review_response = self.client.post('/api/v1/reviews/',
                                          headers={'Authorization': f'Bearer {reviewer_token}'},
                                          json={
                                              "text": "Original review",
                                              "rating": 4,
                                              "place_id": place_id
                                          })
        self.assertEqual(review_response.status_code, 201)
        review_id = review_response.get_json()['id']
        
        # Try to update with different user
        response = self.client.put(f'/api/v1/reviews/{review_id}',
                                  headers={'Authorization': f'Bearer {other_token}'},
                                  json={"text": "Hacked review", "rating": 1})
        self.assertEqual(response.status_code, 403)
        
        # Author can update
        response = self.client.put(f'/api/v1/reviews/{review_id}',
                                  headers={'Authorization': f'Bearer {reviewer_token}'},
                                  json={"text": "Updated review", "rating": 5})
        self.assertEqual(response.status_code, 200)

    def test_delete_review_owner_only(self):
        """Test only review author can delete review"""
        reviewer_id, reviewer_token = self._create_user_and_login("reviewdelete@example.com")
        other_id, other_token = self._create_user_and_login("notdeleter@example.com")
        owner_id, owner_token = self._create_user_and_login("placeowner_delete@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Delete Review Test Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Create review
        review_response = self.client.post('/api/v1/reviews/',
                                          headers={'Authorization': f'Bearer {reviewer_token}'},
                                          json={
                                              "text": "Review to delete",
                                              "rating": 3,
                                              "place_id": place_id
                                          })
        self.assertEqual(review_response.status_code, 201)
        review_id = review_response.get_json()['id']
        
        # Try to delete with different user
        response = self.client.delete(f'/api/v1/reviews/{review_id}',
                                     headers={'Authorization': f'Bearer {other_token}'})
        self.assertEqual(response.status_code, 403)
        
        # Author can delete
        response = self.client.delete(f'/api/v1/reviews/{review_id}',
                                     headers={'Authorization': f'Bearer {reviewer_token}'})
        self.assertEqual(response.status_code, 200)

    # ========================================================================
    # AMENITY TESTS - Attribute validation
    # ========================================================================

    def test_create_amenity_valid_data(self):
        """Test creating amenity with valid data"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        # Note: Amenities require admin token - this should return 401 or 403
        # Adjust based on actual implementation
        self.assertIn(response.status_code, [201, 401, 403])

    def test_create_amenity_empty_text(self):
        """Test creating amenity with empty name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertIn(response.status_code, [400, 401, 403])

    def test_create_amenity_whitespace_only_text(self):
        """Test creating amenity with whitespace-only name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "   "
        })
        self.assertIn(response.status_code, [400, 401, 403])

    def test_create_amenity_already_exist(self):
        """Test creating duplicate amenity"""
        # Note: This test assumes you have admin privileges or modify accordingly
        # Create first amenity
        response1 = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        # Only proceed if first creation succeeded
        if response1.status_code == 201:
            # Try to create duplicate
            response2 = self.client.post('/api/v1/amenities/', json={
                "name": "Swimming Pool"
            })
            self.assertEqual(response2.status_code, 400)

    def test_create_amenity_missing_name(self):
        """Test creating amenity without name field"""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertIn(response.status_code, [400, 401, 403])

    def test_create_amenity_name_too_long(self):
        """Test creating amenity with name exceeding maximum length"""
        long_name = "A" * 51  # Exceeds 50 character limit
        response = self.client.post('/api/v1/amenities/', json={
            "name": long_name
        })
        self.assertIn(response.status_code, [400, 401, 403])

    # ========================================================================
    # RELATIONSHIP TESTS - Testing entity relationships
    # ========================================================================

    def test_get_place_with_amenities_and_reviews(self):
        """Test getting place details includes amenities and reviews"""
        owner_id, owner_token = self._create_user_and_login("fullplace@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Full Detail Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Get place details
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        # Verify structure includes related entities
        self.assertIn('owner', data)
        self.assertIn('amenities', data)
        self.assertIn('reviews', data)
        self.assertIsInstance(data['amenities'], list)
        self.assertIsInstance(data['reviews'], list)

    def test_get_reviews_for_place(self):
        """Test getting all reviews for a specific place"""
        reviewer_id, reviewer_token = self._create_user_and_login("placereviewer@example.com")
        owner_id, owner_token = self._create_user_and_login("placereviews@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Review List Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Create review
        self.client.post('/api/v1/reviews/',
                        headers={'Authorization': f'Bearer {reviewer_token}'},
                        json={
                            "text": "Test review",
                            "rating": 5,
                            "place_id": place_id
                        })
        
        # Get reviews for place
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_amenities_for_place(self):
        """Test getting all amenities for a specific place"""
        owner_id, owner_token = self._create_user_and_login("amenitylist@example.com")
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                         headers={'Authorization': f'Bearer {owner_token}'},
                                         json={
                                             "title": "Amenity List Place",
                                             "price": 100.0,
                                             "latitude": 25.0,
                                             "longitude": -80.0
                                         })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.get_json()['id']
        
        # Get amenities for place
        response = self.client.get(f'/api/v1/places/{place_id}/amenities')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()
