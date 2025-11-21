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

# Start the Flask application
python3 run.py
