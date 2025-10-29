# HBnB - Holberton Project

## Project Description

HBnB is an accommodation rental application developed as part of the Holberton School curriculum. This project implements a complete web application with REST API, business logic layer, and database persistence.

## Objectives

Development of a complete web application following best practices:

- **Layered Architecture**: Separation between presentation, business logic, and data persistence
- **REST API**: RESTful interface with Flask-RESTX
- **UML Modeling**: Technical documentation with UML diagrams
- **Design Patterns**: Repository and Facade patterns
- **Authentication**: JWT-based authentication with password hashing
- **Database**: SQLAlchemy ORM with SQLite

## Architecture

Layered architecture implementation:

```
HBnB Application
├── Presentation Layer (REST API with Flask-RESTX)
├── Business Logic Layer (Models and Facade)
├── Persistence Layer (Repository Pattern)
└── Database Layer (SQLAlchemy with SQLite)
```

## Project Structure

```
holbertonschool-hbnb/
├── README.md                                    # This file
├── HBNB_API.postman_collection.json            # Postman collection for API testing
├── part1/                                      # Phase 1 - Design and modeling
│   ├── README.md                              # Part 1 documentation
│   ├── high-level_package_diagram.mmd        # High-level package diagram
│   ├── business_logic_layer_diagram.mmd      # Business Logic layer diagram
│   ├── sequence_api_call_user.mmd            # Sequence diagram - Users
│   ├── sequence_api_call_place.mmd           # Sequence diagram - Places
│   ├── sequence_api_call_review.mmd          # Sequence diagram - Reviews
│   └── sequence_api_call_request_list.mmd    # Sequence diagram - Lists
├── part2/                                      # Phase 2 - Implementation with in-memory storage
│   └── hbnb/                                  # Main application
│       ├── app/                               # Application package
│       │   ├── api/v1/                       # REST API endpoints
│       │   ├── models/                       # Data models
│       │   ├── services/                     # Business logic (Facade)
│       │   └── persistence/                  # In-memory persistence layer
│       ├── tests/                             # Test suite
│       ├── config.py                         # Application configuration
│       ├── run.py                            # Application entry point
│       └── requirements.txt                  # Python dependencies
└── part3/                                      # Phase 3 - Database and Authentication
    └── hbnb/                                  # Main application
        ├── app/                               # Application package
        │   ├── api/v1/                       # REST API endpoints with auth
        │   ├── models/                       # SQLAlchemy models
        │   ├── services/                     # Business logic (Facade)
        │   └── persistence/                  # SQLAlchemy repository
        ├── sql/                               # SQL schema files
        ├── tests/                             # Test suite
        ├── init_db.py                        # Database initialization
        ├── config.py                         # Configuration with SQLAlchemy
        ├── run.py                            # Application entry point
        └── requirements.txt                  # Python dependencies
```

## Implemented Features

### User Management
- User creation with validation
- Email uniqueness validation
- Password hashing with Bcrypt
- User authentication with JWT tokens
- User profile management (CRUD operations)

### Accommodation Management
- Place creation with validation
- Owner assignment and validation
- Price and location validation (latitude/longitude bounds)
- Place-amenity relationships (many-to-many)
- Place data retrieval and updates

### Amenity System
- Amenity creation and management
- Amenity-place associations
- Name validation and length constraints
- CRUD operations for amenities

### Review System
- Review creation with user and place validation
- Rating system (1-5 scale)
- Text validation
- Review retrieval and management
- CRUD operations for reviews

### Authentication and Security
- JWT token-based authentication
- Login endpoint with email/password validation
- Protected endpoints requiring valid tokens
- Password hashing with Bcrypt
- Role-based access control (is_admin flag)

### Database
- SQLAlchemy ORM with SQLite
- Database models with relationships
- One-to-many relationships (User-Places, User-Reviews, Place-Reviews)
- Many-to-many relationship (Place-Amenities)
- Database initialization script

## Development Status

### Part 1 - Design and Modeling (Completed)

**UML Diagrams:**
- High-level package diagram
- Business Logic class diagram
- API call sequence diagrams (User, Place, Review, Request list)

**Flow Modeling:**
- User interaction flows
- Accommodation management flows
- Review system flows
- List request flows

### Part 2 - Implementation with In-Memory Storage (Completed)

**Business Logic Layer:**
- Complete model implementations (User, Place, Review, Amenity)
- Facade pattern for business operations
- In-memory repository pattern
- Data validation and error handling

**REST API:**
- Flask-RESTX based API
- Complete CRUD operations for all entities
- HTTP status codes and error handling
- API documentation with Swagger

**Architecture Implementation:**
- Layered architecture with clear separation
- Repository pattern for data persistence
- Facade pattern for business logic

**Testing:**
- Automated endpoint tests
- Full test coverage for all API endpoints

### Part 3 - Database and Authentication (Completed)

**Database Integration:**
- SQLAlchemy ORM implementation
- SQLite database (development.db)
- Database models with relationships
- Table schemas in SQL files
- Database initialization script (init_db.py)

**Authentication System:**
- JWT token-based authentication
- Login endpoint (/api/v1/auth/login)
- Protected endpoints with JWT verification
- Password hashing with Bcrypt

**Security Features:**
- Bcrypt password hashing
- JWT token generation and validation
- Role-based access control (is_admin)
- Secure token signing with secret key

**Repository Pattern:**
- SQLAlchemy repository implementation
- Support for both in-memory and database storage
- Abstract repository interface

## Documentation

- **[Part 1 Documentation](./part1/README.md)** - Design and modeling phase
- **[Part 2 Documentation](./part2/hbnb/README.md)** - Implementation with in-memory storage
- **[Part 3 Documentation](./part3/hbnb/README.md)** - Database and authentication implementation

## Technologies

**Backend:**
- Python 3.12
- Flask (Web framework)
- Flask-RESTX (REST API and documentation)
- Flask-JWT-Extended (JWT authentication)
- Flask-Bcrypt (Password hashing)
- SQLAlchemy (ORM)
- Flask-SQLAlchemy (Flask integration)

**Database:**
- SQLite (Development)

**Architecture Patterns:**
- Facade Pattern
- Repository Pattern

**Documentation:**
- Mermaid for UML diagrams
- Swagger UI for API documentation

**Code Quality:**
- PEP 8 compliant

## API Endpoints

### Authentication (Part 3)
- `POST /api/v1/auth/login` - Login with email and password, returns JWT token
- `GET /api/v1/auth/protected` - Protected endpoint requiring valid JWT token

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/<user_id>` - Get a specific user
- `PUT /api/v1/users/<user_id>` - Update a user

### Places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/<place_id>` - Get a specific place
- `PUT /api/v1/places/<place_id>` - Update a place
- `GET /api/v1/places/<place_id>/reviews` - Get all reviews for a place

### Reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/` - Get all reviews
- `GET /api/v1/reviews/<review_id>` - Get a specific review
- `PUT /api/v1/reviews/<review_id>` - Update a review
- `DELETE /api/v1/reviews/<review_id>` - Delete a review

### Amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/<amenity_id>` - Get a specific amenity
- `PUT /api/v1/amenities/<amenity_id>` - Update an amenity

All endpoints return JSON responses with appropriate HTTP status codes.

## About

Project developed as part of the Holberton School curriculum, applying software architecture concepts, web development, and programming best practices.

## License

This project is developed for educational purposes as part of the Holberton School program.
