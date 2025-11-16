"""
Test persistence of data across application restarts.

This module tests that data persisted to the SQLite database
remains available after the application context is closed and reopened.
"""

import unittest
import os
from app import create_app, db
from app.models.user import UserModel
from app.models.place import PlaceModel
from app.models.amenity import AmenityModel
from app.models.review import ReviewModel


class TestDatabasePersistence(unittest.TestCase):
    """Test that data persists across application restarts."""

    def setUp(self):
        """Set up test database before each test."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_persistence.db'
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
            os.remove('test_persistence.db')
        except OSError:
            pass

    def test_user_persists_after_restart(self):
        """Test that a created user persists after app context restart."""
        user_id = None
        
        # Step 1: Create a user in first app context
        with self.app.app_context():
            user = UserModel(
                first_name='John',
                last_name='Doe',
                email='persistence.test@example.com'
            )
            user.hash_password('testpassword123')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
            # Context ends here - simulates app restart

        # Step 2: Create new app context and verify user exists
        with self.app.app_context():
            persisted_user = db.session.get(UserModel, user_id)
            
            self.assertIsNotNone(persisted_user)
            self.assertEqual(persisted_user.first_name, 'John')
            self.assertEqual(persisted_user.last_name, 'Doe')
            self.assertEqual(persisted_user.email, 'persistence.test@example.com')
            self.assertTrue(persisted_user.verify_password('testpassword123'))

    def test_place_persists_after_restart(self):
        """Test that a created place persists after app context restart."""
        place_id = None
        owner_id = None
        
        # Step 1: Create owner and place in first app context
        with self.app.app_context():
            owner = UserModel(
                first_name='Place',
                last_name='Owner',
                email='place.owner@example.com'
            )
            owner.hash_password('password123')
            db.session.add(owner)
            db.session.flush()
            owner_id = owner.id
            
            place = PlaceModel(
                title='Beachfront Villa',
                description='Beautiful villa by the sea',
                price=250.00,
                latitude=25.7617,
                longitude=-80.1918,
                owner_id=owner_id
            )
            db.session.add(place)
            db.session.commit()
            place_id = place.id

        # Step 2: Verify place persists in new context
        with self.app.app_context():
            persisted_place = db.session.get(PlaceModel, place_id)
            
            self.assertIsNotNone(persisted_place)
            self.assertEqual(persisted_place.title, 'Beachfront Villa')
            self.assertEqual(persisted_place.description, 'Beautiful villa by the sea')
            self.assertEqual(float(persisted_place.price), 250.00)
            self.assertEqual(persisted_place.owner_id, owner_id)

    def test_amenity_persists_after_restart(self):
        """Test that a created amenity persists after app context restart."""
        amenity_id = None
        
        # Step 1: Create amenity
        with self.app.app_context():
            amenity = AmenityModel(name='Swimming Pool')
            db.session.add(amenity)
            db.session.commit()
            amenity_id = amenity.id

        # Step 2: Verify amenity persists
        with self.app.app_context():
            persisted_amenity = db.session.get(AmenityModel, amenity_id)
            
            self.assertIsNotNone(persisted_amenity)
            self.assertEqual(persisted_amenity.name, 'Swimming Pool')

    def test_review_persists_after_restart(self):
        """Test that a created review persists after app context restart."""
        review_id = None
        
        # Step 1: Create user, place, and review
        with self.app.app_context():
            owner = UserModel(
                first_name='Owner',
                last_name='User',
                email='owner.review@example.com'
            )
            owner.hash_password('pass123')
            db.session.add(owner)
            db.session.flush()
            
            reviewer = UserModel(
                first_name='Reviewer',
                last_name='User',
                email='reviewer@example.com'
            )
            reviewer.hash_password('pass123')
            db.session.add(reviewer)
            db.session.flush()
            
            place = PlaceModel(
                title='Test Place',
                description='A place to review',
                price=100.00,
                latitude=10.0,
                longitude=20.0,
                owner_id=owner.id
            )
            db.session.add(place)
            db.session.flush()
            
            review = ReviewModel(
                text='Great place to stay!',
                rating=5,
                place_id=place.id,
                user_id=reviewer.id
            )
            db.session.add(review)
            db.session.commit()
            review_id = review.id

        # Step 2: Verify review persists
        with self.app.app_context():
            persisted_review = db.session.get(ReviewModel, review_id)
            
            self.assertIsNotNone(persisted_review)
            self.assertEqual(persisted_review.text, 'Great place to stay!')
            self.assertEqual(persisted_review.rating, 5)

    def test_relationships_persist_after_restart(self):
        """Test that relationships between models persist correctly."""
        owner_id = None
        place_id = None
        
        # Step 1: Create owner with place
        with self.app.app_context():
            owner = UserModel(
                first_name='Relationship',
                last_name='Tester',
                email='relations@example.com'
            )
            owner.hash_password('password')
            db.session.add(owner)
            db.session.flush()
            owner_id = owner.id
            
            place = PlaceModel(
                title='Relationship Test Place',
                description='Testing relationships',
                price=150.00,
                latitude=30.0,
                longitude=40.0,
                owner_id=owner_id
            )
            db.session.add(place)
            db.session.commit()
            place_id = place.id

        # Step 2: Verify relationships load correctly
        with self.app.app_context():
            persisted_place = db.session.get(PlaceModel, place_id)
            persisted_owner = db.session.get(UserModel, owner_id)
            
            # Test forward relationship (place -> owner)
            self.assertIsNotNone(persisted_place.owner)
            self.assertEqual(persisted_place.owner.id, owner_id)
            self.assertEqual(persisted_place.owner.email, 'relations@example.com')
            
            # Test backward relationship (owner -> places)
            self.assertEqual(len(persisted_owner.places), 1)
            self.assertEqual(persisted_owner.places[0].id, place_id)
            self.assertEqual(persisted_owner.places[0].title, 'Relationship Test Place')

    def test_unique_constraints_persist(self):
        """Test that unique constraints are respected across restarts."""
        
        # Step 1: Create user with unique email
        with self.app.app_context():
            user = UserModel(
                first_name='Unique',
                last_name='User',
                email='unique@example.com'
            )
            user.hash_password('password')
            db.session.add(user)
            db.session.commit()

        # Step 2: Try to create duplicate user in new context
        with self.app.app_context():
            duplicate_user = UserModel(
                first_name='Duplicate',
                last_name='Attempt',
                email='unique@example.com'  # Same email
            )
            duplicate_user.hash_password('password')
            db.session.add(duplicate_user)
            
            # Should raise IntegrityError due to unique constraint
            with self.assertRaises(Exception):  # SQLAlchemy will raise IntegrityError
                db.session.commit()

    def test_review_unique_constraint_persists(self):
        """Test that unique constraint on (user_id, place_id) persists."""
        
        user_id = None
        place_id = None
        
        # Step 1: Create user, place, and review
        with self.app.app_context():
            owner = UserModel(
                first_name='Owner',
                last_name='Test',
                email='constraint.owner@example.com'
            )
            owner.hash_password('pass')
            db.session.add(owner)
            db.session.flush()
            
            reviewer = UserModel(
                first_name='Reviewer',
                last_name='Test',
                email='constraint.reviewer@example.com'
            )
            reviewer.hash_password('pass')
            db.session.add(reviewer)
            db.session.flush()
            user_id = reviewer.id
            
            place = PlaceModel(
                title='Constraint Place',
                description='Test constraints',
                price=100.00,
                latitude=10.0,
                longitude=20.0,
                owner_id=owner.id
            )
            db.session.add(place)
            db.session.flush()
            place_id = place.id
            
            review = ReviewModel(
                text='First review',
                rating=4,
                place_id=place_id,
                user_id=user_id
            )
            db.session.add(review)
            db.session.commit()

        # Step 2: Try to create duplicate review in new context
        with self.app.app_context():
            duplicate_review = ReviewModel(
                text='Duplicate review',
                rating=5,
                place_id=place_id,  # Same place
                user_id=user_id     # Same user
            )
            db.session.add(duplicate_review)
            
            # Should raise IntegrityError due to unique constraint
            with self.assertRaises(Exception):
                db.session.commit()


if __name__ == '__main__':
    unittest.main()
