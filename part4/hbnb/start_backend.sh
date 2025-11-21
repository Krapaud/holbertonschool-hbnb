#!/bin/bash
# Script to start the backend API server
# This serves only the API endpoints

echo "======================================"
echo "Starting Backend API Server"
echo "======================================"
echo ""
echo "Backend API will be available at:"
echo "  http://localhost:5000"
echo ""
echo "API Endpoints:"
echo "  - POST /api/v1/auth/login"
echo "  - GET  /api/v1/places"
echo "  - GET  /api/v1/places/<id>"
echo "  - GET  /api/v1/places/<id>/reviews"
echo "  - POST /api/v1/reviews"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

# Change to backend directory
cd backend

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the Flask application
python3 run.py
