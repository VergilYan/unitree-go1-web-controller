#!/bin/bash

# ==============================================================================
# GO1 Web Controller - Frontend Startup Script
# ==============================================================================
# This script starts the frontend HTTP server
# No dependencies needed - just Python!
# ==============================================================================

# ------------------------------
# Configuration
# ------------------------------
# Frontend directory
FRONTEND_DIR="frontend"

# HTTP server port
PORT="8080"

# ------------------------------
# Step 1: Navigate to Frontend Directory
# ------------------------------
echo "=== Starting GO1 Web Controller Frontend ==="
echo "Entering frontend directory..."

# Check if directory exists FIRST (before cd)
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "ERROR: Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

# Now change to the directory
cd $FRONTEND_DIR

# ------------------------------
# Step 2: Start HTTP Server
# ------------------------------
echo "Starting HTTP server on port $PORT..."
echo "Frontend will be available at: http://localhost:$PORT"
echo "Press Ctrl+C to stop the server"
echo ""

# Start Python HTTP server
python -m http.server $PORT
