# HBnB - My Holberton Project

> **Status**: **Under Development**

## What I'm Building

I'm developing HBnB, a style accommodation rental application as part of my Holberton School curriculum. The goal is to create a complete platform for managing accommodations, users, reviews, and amenities.

## My Objectives

This project allows me to develop a complete web application following best practices:

- **Layered Architecture**: Clear separation between presentation, business logic, and data
- **REST API**: Standardized programming interface
- **UML Modeling**: Complete technical documentation with diagrams
- **Design Patterns**: Using patterns like Repository, Facade, etc.

## Architecture I Designed

I opted for a well-defined layered architecture:

```
HBnB Application
├── Presentation Layer (REST API)
├── Business Logic Layer (Domain)
├── Data Access Layer (Repository)
└── Persistence Layer (In-Memory Storage)
```

## My Current Project Structure

```
holbertonschool-hbnb/
├── README.md                                    # This file
├── part1/                                      # Phase 1 - Design and modeling
│   ├── README.md                              # Part 1 documentation
│   ├── high-level_package_diagram.mmd        # High-level package diagram
│   ├── business_logic_layer_diagram.mmd      # Business Logic layer diagram
│   ├── sequence_api_call_user.mmd            # Sequence diagram - Users
│   ├── sequence_api_call_place.mmd           # Sequence diagram - Places
│   ├── sequence_api_call_review.mmd          # Sequence diagram - Reviews
│   └── sequence_api_call_request_list.mmd    # Sequence diagram - Lists
└── part2/                                      # Phase 2 - Implementation
    └── hbnb/                                  # Main application
        ├── app/                               # Application package
        │   ├── api/v1/                       # REST API endpoints
        │   ├── models/                       # Data models
        │   ├── services/                     # Business logic (Facade)
        │   └── persistence/                  # Data persistence layer
        ├── config.py                         # Application configuration
        ├── run.py                            # Application entry point
        └── requirements.txt                  # Python dependencies
```

## Current Features Implemented

### User Management
- User creation and validation
- User profile management
- Email uniqueness validation
- User data retrieval and updates

### Accommodation Management
- Place creation with validation
- Owner assignment and validation
- Place data retrieval and updates
- Price and location validation

### Amenity System
- Amenity creation and management
- Amenity-place associations
- Amenity retrieval operations

### Review System
- Review creation with user and place validation
- Rating system (1-5 scale)
- Review retrieval and management

## Current Development Status

### What I've Already Accomplished

**Part 1 - Design and Modeling:**
1. **UML Diagrams**
   - High-level package diagram
   - Business Logic class diagram
   - API call sequence diagrams

2. **Flow Modeling**
   - User interaction flows
   - Accommodation management flows
   - Review system flows
   - List request flows

**Part 2 - Implementation:**
1. **Business Logic Layer**
   - Complete model implementations (User, Place, Review, Amenity)
   - Facade pattern for business operations
   - In-memory repository pattern
   - Data validation and error handling

2. **REST API**
   - Flask-RESTX based API
   - Complete CRUD operations for all entities
   - Proper HTTP status codes and error handling
   - API documentation with Swagger

3. **Architecture Implementation**
   - Layered architecture with clear separation
   - Repository pattern for data persistence
   - Facade pattern for business logic
   - Proper dependency injection

## Documentation

- **[Part 1 Documentation](./part1/README.md)** - Design and modeling phase
- **[Part 2 Documentation](./part2/hbnb/README.md)** - Implementation phase

## Technologies I'm Using

- **Backend**: Python 3.12 with Flask
- **API Framework**: Flask-RESTX for REST API and documentation
- **Data Persistence**: In-memory repository pattern
- **Architecture Patterns**: Facade, Repository
- **Documentation**: Mermaid for UML diagrams
- **Code Style**: PEP 8 compliant with pycodestyle validation

## API Endpoints

The application provides the following REST API endpoints:

- **Users**: `/api/v1/users/` - CRUD operations for users
- **Places**: `/api/v1/places/` - CRUD operations for places
- **Reviews**: `/api/v1/reviews/` - CRUD operations for reviews
- **Amenities**: `/api/v1/amenities/` - CRUD operations for amenities

All endpoints support standard HTTP methods (GET, POST, PUT, DELETE) where appropriate and return JSON responses.

## About Me

Project developed as part of my **Holberton School** curriculum.

I'm learning and applying software architecture concepts, web development, and programming best practices.

## License

This project is developed for educational purposes as part of the Holberton School program.

---

**Note**: This project is currently in active development. Part 1 (Design) and Part 2 (Implementation) are completed. The application includes a working REST API with in-memory data storage.
