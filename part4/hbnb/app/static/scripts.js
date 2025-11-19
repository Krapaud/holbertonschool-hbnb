/**
 * HBnB Evolution - Main JavaScript File
 * Handles authentication, place listing, filtering, and place details functionality
 */

// ============================================
// DOM CONTENT LOADED - INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  // Get the login form element
  const loginForm = document.getElementById('login-form');

  // If login form exists, attach submit event listener
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      // Get and trim user input values
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
    // Check if user is authenticated
    const token = getCookie('token');
    
    // Only redirect on add_review.html (not on place.html)
    // Check if we're on add_review.html by looking for the specific review textarea ID
    const isAddReviewPage = document.getElementById('review'); // Only exists on add_review.html
    
    if (!token && isAddReviewPage) {
      // Redirect to index if not authenticated and on add_review.html
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

  // Check if user is authenticated on page load
  checkAuthentication();

  // Get the price filter element if it exists
  const priceFilter = document.getElementById('price-filter');

  // If price filter exists, attach change event listener
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      const placeCards = document.querySelectorAll('.place-card');

      // Filter place cards based on selected price
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
// AUTHENTICATION FUNCTIONS
// ============================================

/**
 * Authenticates a user with email and password
 * @param {string} email - User's email address
 * @param {string} password - User's password
 * @returns {Promise<void>}
 */
async function loginUser(email, password) {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    // Store token in cookie and redirect to index page
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

/**
 * Checks if user is authenticated and updates UI accordingly
 * - Manages visibility of login link
 * - Controls display of add review form
 * - Fetches and displays places list on index.html
 * - Fetches and displays place details on place.html
 * @returns {void}
 */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  // Show or hide login link based on authentication status
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
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
 * Retrieves a cookie value by name
 * @param {string} name - Name of the cookie to retrieve
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
  const cookies = document.cookie.split('; ');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split('=');
    if (cookieName === name) {
      return cookieValue;
    }
  }
  return null;
}

// ============================================
// PLACES LIST FUNCTIONS
// ============================================

/**
 * Fetches all places from the API
 * @param {string} token - JWT authentication token
 * @returns {Promise<void>}
 */
async function fetchPlaces(token) {
  const headers = {
    'Content-Type': 'application/json',
  };
  
  // Add Authorization header only if token exists
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  const response = await fetch('/api/v1/places', {
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
 * Creates HTML elements dynamically for each place
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

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
 * @param {string} token - JWT authentication token
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
  
  const response = await fetch(`/api/v1/places/${placeId}`, {
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
 * @param {string} place.name - The name of the place
 * @param {string} place.host - The host's name
 * @param {number} place.price - The price per night
 * @param {string} place.description - The place description
 * @param {string|Array} place.amenities - The available amenities
 */
function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');
  placeDetails.innerHTML = '';
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
    const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
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

    // Use user_name if available, otherwise fallback to user_id
    const authorName = review.user_name || `User ${review.user_id.substring(0, 8)}`;

    article.innerHTML = `
      <h3 class="review-author">${authorName}:</h3>
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
 * @param {string} rating - The rating (1-5)
 * @returns {Promise<void>}
 */
async function submitReview(token, placeId, reviewText, rating) {
  const response = await fetch('/api/v1/reviews', {
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
  } else {
    const errorData = await response.json();
    alert('Failed to submit review: ' + (errorData.error || response.statusText));
  }
}
