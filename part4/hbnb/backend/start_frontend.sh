#!/bin/bash
# Script to start the frontend server
# This serves the static HTML/CSS/JS files

echo "======================================"
echo "Starting Frontend Server"
echo "======================================"
echo ""
echo "Frontend will be available at:"
echo "  http://localhost:8000"
echo ""
echo "Make sure the backend is running on:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

# Change to the static directory
cd static

# Start Python's built-in HTTP server on port 8000
python3 -m http.server 8000
