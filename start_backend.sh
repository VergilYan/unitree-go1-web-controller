#!/bin/bash

# ==============================================================================
# GO1 Web Controller - Backend Startup Script
# ==============================================================================
# This script starts the Flask backend server
# Make sure to activate your conda environment before running
# ==============================================================================

# ------------------------------
# Configuration
# ------------------------------
# Conda environment name (change this to match your environment!)
CONDA_ENV="go1_web"

# Backend directory
BACKEND_DIR="backend"

# Flask app file
FLASK_APP="app.py"

# ------------------------------
# Step 1: Activate Conda Environment
# ------------------------------
echo "=== Starting GO1 Web Controller Backend ==="
echo "Activating Conda environment: $CONDA_ENV"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed or not in PATH!"
    echo "Please install Miniconda/Anaconda first."
    exit 1
fi

# Activate conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $CONDA_ENV

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate conda environment: $CONDA_ENV"
    echo "Please create the environment first with: conda create -n $CONDA_ENV python=3.8"
    exit 1
fi

# ------------------------------
# Step 2: Navigate to Backend Directory
# ------------------------------
echo "Entering backend directory..."

# Check if directory exists FIRST (before cd)
if [ ! -d "$BACKEND_DIR" ]; then
    echo "ERROR: Backend directory not found: $BACKEND_DIR"
    exit 1
fi

# Now change to the directory
cd $BACKEND_DIR

# ------------------------------
# Step 3: Run Flask Server
# ------------------------------
echo "Starting Flask server..."
echo "Server will be available at: http://localhost:5000"
echo "API endpoints: /forward, /backward, /left, /right, /stop, /status"
echo "Press Ctrl+C to stop the server"
echo ""

# Run Flask app
python $FLASK_APP
