#!/usr/bin/env python3
"""Business logic facade module.

This module implements the Facade design pattern, providing a simplified
interface to the complex subsystems (models and repositories). It contains
all business logic and coordinates operations between different components.

The facade acts as a single point of entry for all business operations,
hiding the complexity of model interactions and repository management.
"""
from app.models.amenity import AmenityModel
from app.models.place import PlaceModel
from app.models.review import ReviewModel
from app.models.user import UserModel
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    """Facade class for HBnB business logic.
    
    Implements the Facade design pattern to provide a simplified interface
    for all business operations. Coordinates interactions between models
    and repositories, handling complex business logic in one place.
    
    This class is the single entry point for all business operations,
    ensuring consistency and maintainability.
    
    Attributes:
        user_repo (UserRepository): Repository for user data operations
        amenity_repo (SQLAlchemyRepository): Repository for amenity operations
        review_repo (SQLAlchemyRepository): Repository for review operations
        place_repo (SQLAlchemyRepository): Repository for place operations
    """
    def __init__(self):
        """Initialize the facade with all necessary repositories.
        
        Creates repository instances for each model type.
        UserRepository has custom methods, others use generic SQLAlchemy repo.
        """
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(AmenityModel)
        self.review_repo = SQLAlchemyRepository(ReviewModel)
        self.place_repo = SQLAlchemyRepository(PlaceModel)

    # ==================== USER BUSINESS LOGIC ====================

    def create_user(self, user_data):
        """Create a new user with hashed password.
        
        Args:
            user_data (dict): User information including:
                - first_name (str): User's first name
                - last_name (str): User's last name
                - email (str): User's email address
                - password (str): Plain text password (will be hashed)
                - is_admin (bool, optional): Admin flag
                
        Returns:
            UserModel: The created user instance
        """
        # Create user instance from provided data
        user = UserModel(**user_data)
        # Hash password before storing (never store plain text passwords)
        user.hash_password(user_data['password'])
        # Persist to database
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by their unique ID.
        
        Args:
            user_id (str): UUID of the user to retrieve
            
        Returns:
            UserModel: User instance if found, None otherwise
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by their email address.
        
        Used during login to find user account.
        
        Args:
            email (str): Email address to search for
            
        Returns:
            UserModel: User instance if found, None otherwise
        """
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users in the system.
        
        Returns:
            list[UserModel]: List of all user instances
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user's information.
        
        Args:
            user_id (str): UUID of the user to update
            user_data (dict): Dictionary containing fields to update
            
        Returns:
            UserModel: Updated user instance
        """
        # Update user data in repository
        self.user_repo.update(user_id, user_data)
        # Fetch and return updated user
        return self.user_repo.get(user_id)

    # ==================== AMENITY BUSINESS LOGIC ====================

    def create_amenity(self, amenity_data):
        """Create a new amenity.
        
        Args:
            amenity_data (dict): Amenity information including:
                - name (str): Unique amenity name
                
        Returns:
            AmenityModel: The created amenity instance
        """
        amenity = AmenityModel(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its unique ID.
        
        Args:
            amenity_id (str): UUID of the amenity to retrieve
            
        Returns:
            AmenityModel: Amenity instance if found, None otherwise
        """
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, amenity_name):
        """Retrieve an amenity by its name.
        
        Args:
            amenity_name (str): Name of the amenity to search for
            
        Returns:
            AmenityModel: Amenity instance if found, None otherwise
        """
        return self.amenity_repo.get_by_attribute('name', amenity_name)

    def get_all_amenities(self):
        """Retrieve all amenities in the system.
        
        Returns:
            list[AmenityModel]: List of all amenity instances
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity.
        
        Args:
            amenity_id (str): UUID of the amenity to update
            amenity_data (dict): Dictionary containing fields to update
            
        Returns:
            AmenityModel: Updated amenity instance, or None if not found
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        # Update amenity data and save changes
        amenity.update(amenity_data)
        amenity.save()
        return amenity

    # ==================== PLACE BUSINESS LOGIC ====================

    def create_place(self, place_data):
        """Create a new place with owner validation.
        
        Validates that the owner exists before creating the place.
        
        Args:
            place_data (dict): Place information including:
                - title (str): Place title
                - description (str): Place description
                - price (float): Price per night
                - latitude (float): GPS latitude
                - longitude (float): GPS longitude
                - owner_id (str): UUID of the owner
                
        Returns:
            PlaceModel: The created place instance
            
        Raises:
            ValueError: If owner_id does not match any existing user
        """
        # Validate owner exists in database
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner with id {} not found"
                             .format(place_data['owner_id']))

        # Replace owner_id with actual owner object for relationship
        place_data['owner'] = owner
        del place_data['owner_id']

        # Create and persist place
        place = PlaceModel(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by its unique ID.
        
        Args:
            place_id (str): UUID of the place to retrieve
            
        Returns:
            PlaceModel: Place instance if found, None otherwise
        """
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        """Retrieve a place by its title.
        
        Args:
            title (str): Title of the place to search for
            
        Returns:
            PlaceModel: Place instance if found, None otherwise
        """
        return self.place_repo.get_by_attribute('title', title)

    def get_all_places(self):
        """Retrieve all places in the system.
        
        Returns:
            list[PlaceModel]: List of all place instances
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place.
        
        If owner_id is being updated, validates the new owner exists.
        
        Args:
            place_id (str): UUID of the place to update
            place_data (dict): Dictionary containing fields to update
            
        Returns:
            PlaceModel: Updated place instance, or None if not found
            
        Raises:
            ValueError: If new owner_id does not match any existing user
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # If changing owner, validate new owner exists
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner with id {} not found"
                                 .format(place_data['owner_id']))
            # Replace owner_id with owner object
            place_data['owner'] = owner
            del place_data['owner_id']

        # Update place data and save changes
        place.update(place_data)
        place.save()
        return place

    def add_amenity_to_place(self, place_id, amenity_id):
        """Associate an amenity with a place.
        
        Creates a many-to-many relationship between place and amenity.
        Prevents duplicate associations.
        
        Args:
            place_id (str): UUID of the place
            amenity_id (str): UUID of the amenity
            
        Returns:
            bool: True if association created, False if place/amenity not found
        """
        # Retrieve both place and amenity
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if not place or not amenity:
            return False

        # Add amenity only if not already associated
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            place.save()
        return True

    # ==================== REVIEW BUSINESS LOGIC ====================

    def create_review(self, review_data):
        """Create a review and link it to a place.
        
        Validates that both user and place exist before creating review.
        
        Args:
            review_data (dict): Review information including:
                - user_id (str): UUID of the reviewer
                - place_id (str): UUID of the place being reviewed
                - text (str): Review text
                - rating (int): Rating from 1-5
                
        Returns:
            ReviewModel: The created review instance
        """
        # Extract review data
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        # Fetch user and place (validates they exist)
        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)

        # Create review with relationships
        review = ReviewModel(text=text, rating=rating, place=place, user=user)
        self.review_repo.add(review)

        # Add review to place's reviews list
        place.reviews.append(review)
        place.save()
        return review

    def get_review(self, review_id):
        """Retrieve a review by its unique ID.
        
        Args:
            review_id (str): UUID of the review to retrieve
            
        Returns:
            ReviewModel: Review instance if found, None otherwise
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews in the system.
        
        Returns:
            list[ReviewModel]: List of all review instances
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place.
        
        Args:
            place_id (str): UUID of the place
            
        Returns:
            list[ReviewModel]: List of reviews for the specified place
        """
        # Fetch all reviews and filter by place_id
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews
                if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """Update an existing review.
        
        Args:
            review_id (str): UUID of the review to update
            review_data (dict): Dictionary containing fields to update
            
        Returns:
            ReviewModel: Updated review instance, or None if not found
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None
        # Update review data and save changes
        review.update(review_data)
        review.save()
        return review

    def delete_review(self, review_id):
        """Delete a review from the system.
        
        Args:
            review_id (str): UUID of the review to delete
            
        Returns:
            bool: True if review was deleted, False if not found
        """
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
