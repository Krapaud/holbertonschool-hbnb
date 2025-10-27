# HBnB Application - Part 2

## Project Overview

This is the second part of the HBnB (Holberton Airbnb clone) project, focusing on the implementation of the business logic layer, API endpoints, and in-memory data persistence.

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User API endpoints
│   │       ├── places.py        # Place API endpoints
│   │       ├── reviews.py       # Review API endpoints
│   │       └── amenities.py     # Amenity API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py              # Base model with common attributes
│   │   ├── user.py              # User business logic model
│   │   ├── place.py             # Place business logic model
│   │   ├── review.py            # Review business logic model
│   │   └── amenity.py           # Amenity business logic model
│   ├── services/
│   │   ├── __init__.py          # Facade singleton instance
│   │   └── facade.py            # Facade pattern implementation
│   └── persistence/
│       ├── __init__.py
│       └── repository.py        # In-memory repository implementation
├── tests/
│   ├── __init__.py
│   ├── test_endpoint.py         # Automated endpoint tests
│   └── test_endpoint_report.md  # Test results report
├── run.py                       # Application entry point
├── config.py                    # Environment configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Architecture

This project follows a three-layer architecture:

1. **Presentation Layer** (`app/api/`): REST API endpoints using Flask-RESTX
2. **Business Logic Layer** (`app/models/` and `app/services/`): Domain models and business rules
3. **Persistence Layer** (`app/persistence/`): Data storage and retrieval (currently in-memory)

### Key Components

- **Facade Pattern** (`app/services/facade.py`): Centralized interface for communication between layers
- **Repository Pattern** (`app/persistence/repository.py`): Abstract interface for data persistence with in-memory implementation
- **API Versioning** (`app/api/v1/`): RESTful endpoints organized by version

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

3. **Run the application**:
   ```bash
   python run.py
   ```

4. **Access the API documentation**:
   Open your browser and navigate to `http://localhost:5000/api/v1/`

## Development

### Environment Configuration

The application uses environment-based configuration defined in `config.py`:
- `development`: Debug mode enabled
- `default`: Falls back to development configuration

### API Documentation

The API is documented using Flask-RESTX and is available at `/api/v1/` when the application is running.

### In-Memory Repository

The current implementation uses an in-memory repository for data persistence. This will be replaced with a database-backed solution in Part 3 of the project.

## Dependencies

- **Flask**: Web framework
- **Flask-RESTX**: REST API framework with automatic documentation

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

## Future Enhancements

- Database integration (Part 3)
- User authentication and authorization
- Enhanced error handling and logging

## Contributing

This project is part of the Holberton School curriculum. Follow the project guidelines and coding standards as specified in the course materials.