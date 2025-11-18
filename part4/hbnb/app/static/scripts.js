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
 * Hides login link if user is authenticated
 * Fetches places list if on index page and authenticated
 */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  // Show or hide login link based on authentication status
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }

  // If authenticated and on places list page, fetch places
  if (token && document.getElementById('places-list')) {
    fetchPlaces(token);
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
  const response = await fetch('/api/v1/places', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
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

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  const response = await fetch(`/api/v1/places/${placeId}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (response.ok) {
    const data = await response.json();
    displayPlaceDetails(data);
  } else {
    console.error('Failed to fetch place details');
  }
}

function displayPlaceDetails(place) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

    article.innerHTML = `
      <h1>${place.name}</h1>
      <p>Host: ${place.host}</p>
      <p>Price: $${place.price} per night</p>
      <p>Description: ${place.description}</p>
      <p>Amenities: ${place.amenities}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(article);
  }
