/*
 */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      try {
        await loginUser(email, password);
      } catch (error) {
        alert('Erreur : ' + error.message);
      }
    });
  }

  checkAuthentication();

  document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');

    for (let card of placeCards) {
      const priceText = card.querySelector('p').textContent;
      const price = parseInt(priceText.split('$')[1]);

      if (selectedPrice === 'all') {
        card.style.display = 'block';
      } else if (price <= parseInt(selectedPrice)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    }
  });
});

async function loginUser(email, password) {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }

  if (token && document.getElementById('places-list')) {
    fetchPlaces(token);
  }
}

function getCookie(name) {
  // Function to get a cookie value by its name
  const cookies = document.cookie.split('; ');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split('=');
    if (cookieName === name) {
      return cookieValue;
    }
  }
  return null;
}

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  const response = await fetch('/api/v1/places', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (response.ok) {
    const data = await response.json();
    displayPlaces(data);
  } else {
    console.error('Failed to fetch places');
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '<h2>Available Places</h2>';

  for (let place of places) {
    const article = document.createElement('article');
    article.className = 'place-card';

    article.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price: $${place.price_per_night} per night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(article);
  }
}
