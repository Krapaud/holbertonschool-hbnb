# HBnB Frontend - Part 4

## Project Overview

This is the frontend application for the HBnB (Holberton Airbnb clone) project. It provides a user interface for browsing places, viewing details, managing authentication, and submitting reviews.

## Project Structure

```
frontend/
├── index.html           # Home page with places list and price filter
├── login.html           # Login page for user authentication
├── place.html           # Place details page with reviews
├── add_review.html      # Standalone review submission page
├── scripts.js           # Main JavaScript with API interactions and configuration
├── styles.css           # Application styles
└── images/
    ├── logo.png         # Application logo
    └── favicon.ico      # Browser tab icon
```

## Features

### Pages

#### Home Page (index.html)
- Displays a list of available places fetched from the API
- Price filter dropdown (All, 10, 50, 100)
- Each place card shows title, price, and location
- Click on a place to view details
- Navigation header with logo and login link

#### Login Page (login.html)
- User authentication form with email and password
- JWT token storage in cookies upon successful login
- Redirects to home page after login
- Form validation for required fields

#### Place Details Page (place.html)
- Detailed information about a specific place
- Host information
- Full description
- Price and location details
- List of amenities
- Reviews section with all reviews for the place
- Add review form (visible only when authenticated)
- Rating selection (1-5 stars)

#### Add Review Page (add_review.html)
- Standalone page for submitting reviews
- Review text area
- Rating dropdown with star display
- Requires authentication (redirects if not logged in)

### JavaScript Functionality (scripts.js)

#### Authentication
- `checkAuthentication()`: Verifies if user is logged in
- `loginUser(email, password)`: Handles login API call
- `getCookie(name)`: Retrieves token from cookies
- Login link visibility control based on authentication status

#### Places Management
- Fetch and display all places on home page
- Price filtering functionality
- Dynamic place card creation
- Click handlers for navigation to place details

#### Place Details
- Fetch individual place information by ID
- Display host details
- Show amenities list
- Load and display reviews

#### Reviews Management
- `submitReview(token, placeId, text, rating)`: Submit new review
- Display reviews with user and rating information
- Form validation for review text and rating
- Authentication check before submission

#### Utility Functions
- `getPlaceIdFromURL()`: Extract place ID from URL parameters
- Cookie management for JWT tokens
- Dynamic content population
- Error handling and user feedback

## API Integration

The frontend communicates with the backend API at `http://localhost:5000` (configurable directly in `scripts.js`).

### API Endpoints Used

#### Authentication
- `POST /api/v1/auth/login` - User login with email and password

#### Places
- `GET /api/v1/places` - Retrieve all places
- `GET /api/v1/places/<place_id>` - Get specific place details

#### Reviews
- `GET /api/v1/places/<place_id>/reviews` - Get reviews for a place
- `POST /api/v1/reviews` - Submit a new review (requires authentication)

#### Users
- `GET /api/v1/users/<user_id>` - Get user information for review display

## Setup and Installation

### Prerequisites
- Python 3.12 or higher (for running the development server)
- Backend API running on `http://localhost:5000`

### Running the Frontend

#### Option 1: Using the provided script
```bash
# From the part4/hbnb directory
./start_frontend.sh
```

#### Option 2: Manual start
```bash
# Navigate to the frontend directory
cd frontend

# Start a simple HTTP server
python3 -m http.server 8000
```

The frontend will be available at `http://localhost:8000`

### Configuration

The API base URL is defined at the top of `scripts.js`. To change it, edit the constant:
```javascript
// At the top of scripts.js
const API_BASE_URL = 'http://localhost:5000';
```

## User Flow

### Browsing Places (Unauthenticated)
1. User visits home page
2. Views list of available places
3. Can filter by maximum price
4. Clicks on a place to view details
5. Views place information, amenities, and reviews

### Authentication Flow
1. User clicks "Login" in navigation
2. Enters email and password
3. Upon successful login, JWT token is stored in cookies
4. Login link disappears from navigation
5. User is redirected to home page

### Submitting a Review (Authenticated)
1. User logs in
2. Navigates to a place details page
3. Scrolls to "Add a Review" section
4. Enters review text and selects rating (1-5 stars)
5. Submits the form
6. Review is posted to the API with JWT authentication
7. Page refreshes to show the new review

## Features by Authentication State

### Unauthenticated Users Can:
- Browse all places
- Filter places by price
- View place details
- View place reviews
- View amenities

### Authenticated Users Can Also:
- Submit reviews for places
- Access authenticated-only pages

## Technical Details

### Cookie Management
- JWT tokens are stored in cookies with 7-day expiration
- Token is automatically included in authenticated API requests
- Cookies are used to maintain login state across page navigation

### Error Handling
- Form validation for required fields
- API error messages displayed via alerts
- Graceful handling of authentication failures
- Redirection to login page when authentication is required

### Dynamic Content
- All places, reviews, and details are loaded dynamically via API calls
- No page reloads for content updates
- Responsive updates based on user actions

## Browser Compatibility

The application uses standard HTML5, CSS3, and ES6 JavaScript features:
- Async/await for API calls
- Fetch API for HTTP requests
- Modern DOM manipulation
- CSS Flexbox and Grid for layouts

Recommended browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Notes

### CORS Configuration
The backend must have CORS enabled to allow requests from the frontend server:
```python
from flask_cors import CORS
CORS(app)
```

### Security Considerations
- Passwords are never stored in the frontend
- JWT tokens are stored in cookies (not localStorage for better security)
- All authenticated requests include the JWT token in headers
- Sensitive operations require valid authentication

## Known Limitations

- No user registration interface (users must be created via API or admin)
- No profile management page
- No place creation interface
- No amenity management
- Reviews cannot be edited or deleted from the UI
- No pagination for places or reviews

## Future Enhancements

Potential improvements for future versions:
- User registration page
- User profile page with edit functionality
- Place creation and management interface
- Review edit and delete functionality
- Pagination for places and reviews
- Advanced filtering (by location, amenities, etc.)
- Search functionality
- Image uploads for places
- Real-time updates with WebSockets

## Contributing

This project is part of the Holberton School curriculum. Follow the project guidelines and coding standards as specified in the course materials.
