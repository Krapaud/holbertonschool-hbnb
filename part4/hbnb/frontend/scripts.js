/**
 * HBnB Main JavaScript File
 * This file manages:
 * - User login and logout
 * - Display of the places list
 * - Details of a place
 * - Reviews
 */

// The address of our backend API
const API_BASE_URL = 'http://localhost:5000';

// ============================================
// STARTUP - Code executed when the page loads
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  // Get the login form if it exists
  const loginForm = document.getElementById('login-form');

  // If the login form exists on the page
  if (loginForm) {
    // Listen for when the user submits the form
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault(); // Prevents page reload

      // Get the email and password entered by the user
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      try {
        await loginUser(email, password);
      } catch (error) {
        alert('Error: ' + error.message);
      }
    });
  }

  // Handle review form submission
  const reviewForm = document.getElementById('review-form');
  
  if (reviewForm) {
    // Check if the user is logged in
    const token = getCookie('token');
    
    // Check if we're on the add_review.html page
    const isAddReviewPage = document.getElementById('review');
    
    if (!token && isAddReviewPage) {
      // If not logged in on add_review.html, redirect to home
      window.location.href = 'index.html';
      return;
    }
    
    const placeId = getPlaceIdFromURL();
    
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      
      // Get review text and rating from form
      // Handle both 'review' (add_review.html) and 'review-text' (place.html)
      const reviewTextElement = document.getElementById('review') || document.getElementById('review-text');
      const reviewText = reviewTextElement ? reviewTextElement.value : '';
      const ratingElement = document.getElementById('rating');
      const rating = ratingElement ? ratingElement.value : '';
      
      // Make AJAX request to submit review
      try {
        await submitReview(token, placeId, reviewText, rating);
      } catch (error) {
        alert('Error submitting review: ' + error.message);
      }
    });
  }

  // Check if the user is logged in
  checkAuthentication();

  // Get the price filter if it exists
  const priceFilter = document.getElementById('price-filter');

  // If the filter exists, listen for changes
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value; // The selected price
      const placeCards = document.querySelectorAll('.place-card'); // All places

      // Filter places based on the selected price
      for (let card of placeCards) {
        const priceText = card.querySelector('p').textContent;
        const price = parseInt(priceText.split('$')[1]);

        // Show or hide cards based on filter selection
        if (selectedPrice === 'all') {
          card.style.display = 'block';
        } else if (price <= parseInt(selectedPrice)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      }
    });
  }
});

// ============================================
// LOGIN AND LOGOUT FUNCTIONS
// ============================================

/**
 * Logs in a user with their email and password
 * @param {string} email - The user's email address
 * @param {string} password - The user's password
 */
async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    // If login succeeds, save the token and redirect
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`; // Save the token
    window.location.href = 'index.html'; // Redirect to home page
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

/**
 * Checks if the user is logged in and updates the interface
 * This function:
 * - Shows "Login" or "Logout" based on login status
 * - Shows/hides the add review form
 * - Loads the places list on the home page
 * - Loads place details on its page
 */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  // Show or hide login link based on authentication status
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
      loginLink.textContent = 'Login';
      loginLink.href = 'login.html';
      loginLink.onclick = null;
    } else {
      loginLink.style.display = 'block';
      loginLink.textContent = 'Logout';
      loginLink.href = '#';
      loginLink.addEventListener('click', (e) => {
        e.preventDefault();
        logout();
      });
    }
  }

  // Show or hide add review section based on authentication status
  if (addReviewSection) {
    if (token) {
      addReviewSection.style.display = 'block';
    } else {
      addReviewSection.style.display = 'none';
    }
  }

  // If on places list page, fetch places (with token if available)
  if (document.getElementById('places-list')) {
    fetchPlaces(token);
  }

  // If on place details page, fetch and display place details
  if (document.getElementById('place-details')) {
    // Extract place ID from URL query parameters
    const placeId = getPlaceIdFromURL();
    
    if (placeId) {
      // Fetch place details (with token if available)
      fetchPlaceDetails(token, placeId);
      // Fetch reviews for this place
      fetchPlaceReviews(placeId);
    } else {
      // Display error if no place ID in URL
      document.getElementById('place-details').innerHTML = '<p>Error: No place ID provided in URL.</p>';
    }
  }
}

/**
 * Logs out the user by removing their token
 * and redirects to the home page
 */
function logout() {
  // Delete the cookie by making it expire in the past
  document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  // Redirect to home page
  window.location.href = 'index.html';
}

/**
 * Gets the value of a cookie by its name
 * @param {string} name - The name of the cookie to search for
 * @returns {string|null} The cookie value, or null if not found
 */
function getCookie(name) {
  // Split all cookies
  const cookies = document.cookie.split('; ');
  // Search for the cookie we want
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split('=');
    if (cookieName === name) {
      return cookieValue;
    }
  }
  return null;
}

// ============================================
// FUNCTIONS FOR PLACES LIST
// ============================================

/**
 * Fetches all places from the API
 * @param {string|null} token - The login token (optional)
 */
async function fetchPlaces(token) {
  const headers = {
    'Content-Type': 'application/json',
  };
  
  // Add Authorization header only if token exists
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE_URL}/api/v1/places/`, {
    method: 'GET',
    headers: headers,
  });

  if (response.ok) {
    const data = await response.json();
    console.log('Places received:', data);
    console.log('Number of places:', data.length);
    displayPlaces(data);
  } else {
    console.error('Failed to fetch places');
  }
}

/**
 * Displays the list of places on the page
 * @param {Array} places - The list of places to display
 */
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = ''; // Clear the current list

  // Create a card for each place
  for (let place of places) {
    const article = document.createElement('article');
    article.className = 'place-card';

    article.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price} per night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(article);
  }
}

// ============================================
// PLACE DETAILS FUNCTIONS
// ============================================

/**
 * Extracts the place ID from the URL query parameters
 * @returns {string|null} The place ID from the URL, or null if not found
 */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

/**
 * Fetches detailed information about a specific place from the API
 * @param {string|null} token - JWT authentication token (optional)
 * @param {string} placeId - The unique identifier of the place
 * @returns {Promise<void>}
 */
async function fetchPlaceDetails(token, placeId) {
  const headers = {
    'Content-Type': 'application/json',
  };
  
  // Add Authorization header only if token exists
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}`, {
    method: 'GET',
    headers: headers,
  });

  if (response.ok) {
    const data = await response.json();
    console.log('Place details received:', data);
    displayPlaceDetails(data);
  } else {
    console.error('Failed to fetch place details');
  }
}

/**
 * Displays detailed information about a place on the page
 * Creates and populates HTML elements dynamically with place data
 * @param {Object} place - The place object containing all details
 * @param {string} place.title - The title of the place
 * @param {Object} place.owner - The owner object with first_name and last_name
 * @param {number} place.price - The price per night
 * @param {string} place.description - The place description
 * @param {Array} place.amenities - Array of amenity objects with name property
 */
function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');
  placeDetails.innerHTML = '';

  // Create article element to contain place information
  const article = document.createElement('article');
  article.className = 'place-info';

  // Get host name
  let hostName = 'Unknown';
  if (place.owner) {
    hostName = place.owner.first_name + ' ' + place.owner.last_name;
  }

  // Get amenities list
  let amenitiesList = 'None';
  if (place.amenities && place.amenities.length > 0) {
    amenitiesList = '';
    for (let i = 0; i < place.amenities.length; i++) {
      amenitiesList = amenitiesList + place.amenities[i].name;
      if (i < place.amenities.length - 1) {
        amenitiesList = amenitiesList + ', ';
      }
    }
  }

  // Populate article with place details
  article.innerHTML = `
      <h1>${place.title}</h1>
      <p><strong>Host:</strong> ${hostName}</p>
      <p><strong>Price per night:</strong> $${place.price}</p>
      <p><strong>Description:</strong> ${place.description}</p>
      <p><strong>Amenities:</strong> ${amenitiesList}</p>
    `;

  // Append the created article to the place details section
  placeDetails.appendChild(article);
}

// ============================================
// REVIEWS DISPLAY FUNCTIONS
// ============================================

/**
 * Fetches all reviews for a specific place from the API
 * @param {string} placeId - The unique identifier of the place
 * @returns {Promise<void>}
 */
async function fetchPlaceReviews(placeId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}/reviews`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const reviews = await response.json();
      console.log('Reviews received:', reviews);
      displayReviews(reviews);
    } else {
      console.error('Failed to fetch reviews');
      document.getElementById('reviews-list').innerHTML = '<p>Unable to load reviews.</p>';
    }
  } catch (error) {
    console.error('Error fetching reviews:', error);
    document.getElementById('reviews-list').innerHTML = '<p>Error loading reviews.</p>';
  }
}

/**
 * Displays reviews on the page
 * Creates HTML elements dynamically for each review
 * @param {Array} reviews - Array of review objects
 * @param {string} reviews[].id - Review ID
 * @param {string} reviews[].text - Review text
 * @param {number} reviews[].rating - Review rating (1-5)
 * @param {string} reviews[].user_id - ID of the user who wrote the review
 */
function displayReviews(reviews) {
  const reviewsList = document.getElementById('reviews-list');
  reviewsList.innerHTML = '';

  // Check if there are any reviews
  if (!reviews || reviews.length === 0) {
    reviewsList.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review this place!</p>';
    return;
  }

  // Create a card for each review
  for (let review of reviews) {
    const article = document.createElement('article');
    article.className = 'review-card';

    // Convert rating number to stars
    const stars = getStarRating(review.rating);

    article.innerHTML = `
      <h3 class="review-author">${review.user_name}</h3>
      <p class="review-comment">"${review.text}"</p>
      <p class="review-rating">Rating: ${stars}</p>
    `;

    reviewsList.appendChild(article);
  }
}

/**
 * Converts a numeric rating to star symbols
 * @param {number} rating - Rating value (1-5)
 * @returns {string} Star symbols representing the rating
 */
function getStarRating(rating) {
  const fullStar = '★';
  const emptyStar = '☆';
  let stars = '';
  
  for (let i = 1; i <= 5; i++) {
    if (i <= rating) {
      stars += fullStar;
    } else {
      stars += emptyStar;
    }
  }
  
  return stars;
}

// ============================================
// REVIEW SUBMISSION FUNCTIONS
// ============================================

/**
 * Submits a review for a place
 * @param {string} token - JWT authentication token
 * @param {string} placeId - The place ID
 * @param {string} reviewText - The review text
 * @param {string} rating - The rating as string (will be converted to integer)
 * @returns {Promise<void>}
 */
async function submitReview(token, placeId, reviewText, rating) {
  const response = await fetch(`${API_BASE_URL}/api/v1/reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      text: reviewText,
      rating: parseInt(rating),
      place_id: placeId
    }),
  });

  if (response.ok) {
    alert('Review submitted successfully!');
    document.getElementById('review-form').reset();
    
    // Refresh reviews list if on place details page
    if (document.getElementById('reviews-list')) {
      fetchPlaceReviews(placeId);
    }
    
    // Redirect to place details page if on add_review.html
    if (document.getElementById('review')) {
      window.location.href = `place.html?id=${placeId}`;
    }
  } else {
    const errorData = await response.json();
    alert('Failed to submit review: ' + (errorData.error || response.statusText));
  }
}
