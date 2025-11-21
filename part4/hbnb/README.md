# HBnB Application - Part 4

## Project Overview

This is the fourth part of the HBnB (Holberton Airbnb clone) project, implementing a complete full-stack web application with a separated backend API and frontend interface.

## Architecture

This part implements a **client-server architecture** with clear separation between frontend and backend:

```
HBnB Full-Stack Application
├── Backend (API Server)
│   ├── Flask REST API with CORS
│   ├── SQLAlchemy ORM
│   ├── JWT Authentication
│   └── Port 5000
└── Frontend (Static Web Application)
    ├── HTML/CSS/JavaScript
    ├── Fetch API for HTTP requests
    ├── Cookie-based JWT storage
    └── Port 8000
```

## Project Structure

```
part4/hbnb/
├── backend/                    # Backend API server
│   ├── app/                   # Application package
│   │   ├── api/v1/           # REST API endpoints
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic (Facade)
│   │   └── persistence/      # Data repositories
│   ├── sql/                   # SQL schema files
│   ├── tests/                 # Test suite
│   ├── init_db.py            # Database initialization
│   ├── run.py                # Backend entry point
│   ├── requirements.txt      # Python dependencies
│   ├── start_backend.sh      # Backend startup script
│   └── README.md             # Backend documentation
├── frontend/                  # Frontend application
│   ├── index.html            # Home page with places list
│   ├── login.html            # Login page
│   ├── place.html            # Place details page
│   ├── add_review.html       # Review submission page
│   ├── scripts.js            # Main JavaScript
│   ├── styles.css            # Application styles
│   ├── images/               # Images (logo, icons, favicon)
│   └── README.md             # Frontend documentation
├── start_backend.sh           # Start backend server
├── start_frontend.sh          # Start frontend server
└── README.md                  # This file
```

## Features

### Backend API
- RESTful API with Flask-RESTX
- JWT token-based authentication
- SQLAlchemy ORM with SQLite database
- Bcrypt password hashing
- CORS support for cross-origin requests
- Comprehensive API documentation with Swagger UI
- Role-based access control (user/admin)

### Frontend Application
- Responsive web interface
- User authentication with login
- Places listing with price filtering
- Place details with reviews
- Review submission functionality
- JWT token management via cookies
- Dynamic content loading

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Web browser (Chrome, Firefox, Safari, Edge)

## Installation and Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python3 init_db.py
   ```

### Running the Application

You need to run both backend and frontend servers simultaneously.

#### Option 1: Using the startup scripts (Recommended)

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```
The backend API will be available at `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```
The frontend will be available at `http://localhost:8000`

#### Option 2: Manual start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python3 run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 8000
```

### Accessing the Application

Once both servers are running:
- **Frontend Application**: `http://localhost:8000`
- **Backend API**: `http://localhost:5000`
- **API Documentation (Swagger UI)**: `http://localhost:5000/api/v1/`

## Application Flow

### 1. Browsing Places (Unauthenticated)
- Visit `http://localhost:8000`
- View all available places
- Filter places by maximum price
- Click on a place to view details
- See reviews for each place

### 2. User Authentication
- Click "Login" in the navigation
- Enter email and password
- Upon successful login, JWT token is stored in cookies
- Login link disappears from navigation

### 3. Submitting Reviews (Authenticated)
- Log in to the application
- Navigate to a place details page
- Scroll to "Add a Review" section
- Enter review text and select rating (1-5 stars)
- Submit the form
- New review appears on the page

## API Endpoints

The backend provides the following REST API endpoints:

### Authentication
- `POST /api/v1/auth/login` - User login

### Users
- `POST /api/v1/users` - Create user (registration)
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/<id>` - Get specific user
- `PUT /api/v1/users/<id>` - Update user

### Places
- `POST /api/v1/places` - Create place (authenticated)
- `GET /api/v1/places` - Get all places
- `GET /api/v1/places/<id>` - Get specific place
- `PUT /api/v1/places/<id>` - Update place (owner/admin)
- `GET /api/v1/places/<id>/reviews` - Get place reviews
- `POST /api/v1/places/<id>/amenities` - Add amenity to place (owner/admin)

### Reviews
- `POST /api/v1/reviews` - Create review (authenticated)
- `GET /api/v1/reviews` - Get all reviews
- `GET /api/v1/reviews/<id>` - Get specific review
- `PUT /api/v1/reviews/<id>` - Update review (author/admin)
- `DELETE /api/v1/reviews/<id>` - Delete review (author/admin)

### Amenities
- `POST /api/v1/amenities` - Create amenity (admin only)
- `GET /api/v1/amenities` - Get all amenities
- `GET /api/v1/amenities/<id>` - Get specific amenity
- `PUT /api/v1/amenities/<id>` - Update amenity (admin only)

## Technologies Used

### Backend
- **Python 3.12**
- **Flask** - Web framework
- **Flask-RESTX** - REST API and documentation
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin resource sharing
- **SQLAlchemy** - ORM
- **SQLite** - Database

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (ES6+)** - Logic and interactivity
- **Fetch API** - HTTP requests

## Testing

The backend includes a comprehensive test suite with 86 tests covering:
- API endpoints (51 tests)
- Core model classes (28 tests)
- Database persistence (7 tests)

Run tests from the backend directory:
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

## Security Features

- **JWT Authentication**: Token-based authentication for protected endpoints
- **Password Hashing**: Bcrypt hashing for user passwords
- **CORS Configuration**: Controlled cross-origin access
- **Role-Based Access Control**: User and admin roles
- **Ownership Verification**: Users can only modify their own resources

## Development Notes

### CORS Configuration
The backend has CORS enabled to allow requests from the frontend server. This is necessary because the frontend and backend run on different ports (8000 and 5000).

### Cookie Management
JWT tokens are stored in cookies with 7-day expiration for persistent authentication across sessions.

### API Base URL
The frontend API base URL is configured in `frontend/scripts.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

Change this value if deploying to a different environment.

## Troubleshooting

### Port Already in Use
If port 5000 or 8000 is already in use:
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

### Database Issues
If you encounter database errors, reinitialize the database:
```bash
cd backend
rm -f instance/development.db
python3 init_db.py
```

### CORS Errors
If you see CORS errors in the browser console:
- Ensure both backend and frontend are running
- Verify the API_BASE_URL in scripts.js matches the backend URL
- Check that Flask-CORS is properly installed

## Documentation

For detailed documentation:
- **Backend Documentation**: See `backend/README.md`
- **Frontend Documentation**: See `frontend/README.md`

## Contributing

This project is part of the Holberton School curriculum. Follow the project guidelines and coding standards as specified in the course materials.
