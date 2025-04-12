#!/bin/bash

# IntelliShop Project Runner
# This script sets up and runs the IntelliShop web application
#
# === USAGE INSTRUCTIONS ===
# How to run:
#   1. Make this script executable: chmod +x build.sh
#   2. Run the script in WSL terminal: ./build.sh
#
# How to close:
#   - Press Ctrl+C in the terminal to stop the server
# ===========================

# Logging function
log() {
    echo "[$(date)] $1"
}

log "Starting IntelliShop setup"

# Configuration
PORT=8000
VENV_DIR=".venv"

# Check if virtual environment exists and activate it
if [ -d "$VENV_DIR" ]; then
    log "Activating virtual environment"
    source $VENV_DIR/bin/activate
    if [ $? -ne 0 ]; then
        log "ERROR: Failed to activate virtual environment"
        exit 1
    fi
else
    log "WARNING: Virtual environment not found. Using system Python"
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    log "ERROR: Python3 is not installed or not in PATH"
    exit 1
fi

# Start the server
log "Starting HTTP server on port $PORT"
log "Visit http://localhost:$PORT in your browser"
log "Press Ctrl+C to stop the server"

# Run the HTTP server
python3 -m http.server $PORT

# This line will execute when the user presses Ctrl+C
log "Server shutdown complete" 