````markdown
# HBnB Application - Part 3

## Project Overview

This is the third part of the HBnB (Holberton Airbnb clone) project, focusing on database persistence with SQLAlchemy, authentication with JWT, and password hashing.

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py              # Flask application factory with SQLAlchemy, Bcrypt and JWT
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User API endpoints
│   │       ├── places.py        # Place API endpoints
│   │       ├── reviews.py       # Review API endpoints
│   │       ├── amenities.py     # Amenity API endpoints
│   │       └── auth.py          # Authentication endpoints (login, protected)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py              # Base model with SQLAlchemy
│   │   ├── user.py              # User model with password hashing
│   │   ├── place.py             # Place model with relationships
│   │   ├── review.py            # Review model
│   │   └── amenity.py           # Amenity model
│   ├── services/
│   │   ├── __init__.py          # Facade singleton instance
│   │   └── facade.py            # Facade pattern implementation
│   └── persistence/
│       ├── __init__.py
│       └── repository.py        # SQLAlchemy and In-memory repository implementations
├── sql/
│   ├── users.sql                # Users table schema
│   ├── places.sql               # Places table schema
│   ├── reviews.sql              # Reviews table schema
│   ├── amenities.sql            # Amenities table schema
│   ├── place_amenity.sql        # Many-to-many relationship table
│   └── insert_data.sql          # Sample data
├── tests/
│   ├── __init__.py
│   ├── test_endpoint.py         # Automated endpoint tests
│   └── test_endpoint_report.md  # Test results report
├── init_db.py                   # Database initialization script
├── run.py                       # Application entry point
├── config.py                    # Environment configuration with SQLAlchemy settings
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Architecture

This project follows a three-layer architecture:

1. **Presentation Layer** (`app/api/`): REST API endpoints using Flask-RESTX with JWT authentication
2. **Business Logic Layer** (`app/models/` and `app/services/`): Domain models with SQLAlchemy and business rules
3. **Persistence Layer** (`app/persistence/`): Data storage with SQLAlchemy repository pattern

### Key Components

- **Facade Pattern** (`app/services/facade.py`): Centralized interface for communication between layers
- **Repository Pattern** (`app/persistence/repository.py`): Abstract interface with SQLAlchemy and in-memory implementations
- **API Versioning** (`app/api/v1/`): RESTful endpoints organized by version
- **Authentication** (`app/api/v1/auth.py`): JWT-based authentication with login and protected endpoints
- **Password Security** (`app/models/user.py`): Bcrypt password hashing

### Key Features

- **SQLAlchemy ORM**: Database models with relationships (User, Place, Review, Amenity)
- **JWT Authentication**: Secure token-based authentication with role-based access (is_admin)
- **Password Hashing**: Bcrypt for secure password storage
- **Database Relationships**: One-to-many and many-to-many relationships between models
- **SQL Schema**: Pre-defined SQL scripts for table creation and sample data

## Installation and Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   python init_db.py
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

5. **Access the API documentation**:
   Open your browser and navigate to `http://localhost:5000/api/v1/`

## Development

### Environment Configuration

The application uses environment-based configuration defined in `config.py`:
- `development`: Debug mode enabled with SQLite database (`development.db`)
- SQLAlchemy configuration with automatic database URI setup
- Secret key for JWT token generation

### Database Models

All models inherit from `BaseModel` which provides:
- UUID primary key
- created_at and updated_at timestamps
- SQLAlchemy declarative base

**Relationships:**
- User has many Places (one-to-many)
- User has many Reviews (one-to-many)
- Place has many Reviews (one-to-many)
- Place has many Amenities (many-to-many via place_amenity table)

### API Documentation

The API is documented using Flask-RESTX and is available at `/api/v1/` when the application is running.

## Dependencies

- **Flask**: Web framework
- **Flask-RESTX**: REST API framework with automatic documentation
- **Flask-JWT-Extended**: JWT token authentication
- **Flask-Bcrypt**: Password hashing
- **SQLAlchemy**: ORM for database interactions
- **Flask-SQLAlchemy**: Flask integration for SQLAlchemy

## Testing

The project includes comprehensive automated tests for all API endpoints.

### Test Results Summary

**API Testing Report - October 17, 2025**

- **Total tests:** 27
- **Successful tests:** 27
- **Failed tests:** 0
- **Success rate:** 100%

### Test Suites

#### test_endpoint.py (27 tests)
**Purpose:** Validates endpoint functionality and data validation

**Test Categories:**
- **User Endpoints (8 tests):** User creation, validation for empty/whitespace fields, email format validation, missing required fields, duplicate email handling
- **Place Endpoints (7 tests):** Place creation, title validation, price validation (negative/zero values), geographic coordinates validation (latitude: -90 to 90, longitude: -180 to 180)
- **Review Endpoints (6 tests):** Review creation, text validation, user/place ID validation, rating validation (1-5)
- **Amenity Endpoints (6 tests):** Amenity creation, name validation, duplicate detection, missing fields, name length validation (max 50 characters)

### Key Validations Implemented
- **Email Format:** Comprehensive regex validation
- **Geographic Coordinates:** Proper latitude/longitude bounds
- **Data Integrity:** Required field validation and type checking
- **Error Handling:** Appropriate HTTP status codes (400 for validation errors, 404 for not found, 409 for conflicts)
- **Type Safety:** Strict type validation for all inputs
- **Boundary Testing:** Extreme values and edge cases handled correctly

### Running Tests

To run all the automated tests:
```bash
# Activate virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_endpoint.py -v
```

For detailed test results, see `tests/test_endpoint_report.md`.

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login with email and password, returns JWT token
- `GET /api/v1/auth/protected` - Protected endpoint requiring valid JWT token

### Users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/<user_id>` - Get a specific user
- `PUT /api/v1/users/<user_id>` - Update a user

### Places
- `POST /api/v1/places` - Create a new place
- `GET /api/v1/places` - Get all places
- `GET /api/v1/places/<place_id>` - Get a specific place
- `PUT /api/v1/places/<place_id>` - Update a place
- `GET /api/v1/places/<place_id>/reviews` - Get all reviews for a place

### Reviews
- `POST /api/v1/reviews` - Create a new review
- `GET /api/v1/reviews` - Get all reviews
- `GET /api/v1/reviews/<review_id>` - Get a specific review
- `PUT /api/v1/reviews/<review_id>` - Update a review
- `DELETE /api/v1/reviews/<review_id>` - Delete a review

### Amenities
- `POST /api/v1/amenities` - Create a new amenity
- `GET /api/v1/amenities` - Get all amenities
- `GET /api/v1/amenities/<amenity_id>` - Get a specific amenity
- `PUT /api/v1/amenities/<amenity_id>` - Update an amenity

## API Documentation

The API is fully documented using Flask-RESTX and Swagger UI:
- Access the interactive documentation at `http://localhost:5000/api/v1/`
- All endpoints include proper schemas and response codes
- Complete data model definitions
- JWT authentication endpoints for secure access

## Security Features

- **Password Hashing**: User passwords are hashed using Bcrypt before storage
- **JWT Authentication**: Token-based authentication for protected endpoints
- **Role-Based Access**: Admin flag in JWT claims for role-based authorization
- **Secure Token Generation**: Secret key configuration for JWT token signing

## Database

- **Database Engine**: SQLite (development.db)
- **ORM**: SQLAlchemy with declarative models
- **Initialization**: `init_db.py` script creates all tables
- **SQL Scripts**: Pre-defined schemas in `sql/` directory for reference

## Contributing

This project is part of the Holberton School curriculum. Follow the project guidelines and coding standards as specified in the course materials.
````