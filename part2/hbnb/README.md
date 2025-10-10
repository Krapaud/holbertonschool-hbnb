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
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User API endpoints
│   │       ├── places.py        # Place API endpoints
│   │       ├── reviews.py       # Review API endpoints
│   │       ├── amenities.py     # Amenity API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User business logic model
│   │   ├── place.py             # Place business logic model
│   │   ├── review.py            # Review business logic model
│   │   ├── amenity.py           # Amenity business logic model
│   ├── services/
│   │   ├── __init__.py          # Facade singleton instance
│   │   ├── facade.py            # Facade pattern implementation
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py        # In-memory repository implementation
├── run.py                       # Application entry point
├── config.py                    # Environment configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
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

## Future Enhancements

- Database integration (Part 3)
- User authentication and authorization
- File upload capabilities
- Caching mechanisms
- Comprehensive testing suite

## Contributing

This project is part of the Holberton School curriculum. Follow the project guidelines and coding standards as specified in the course materials.