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

# Logging function with timestamp
log() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1"
}

error() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERROR: $1" >&2
    exit 1
}

# Global variables for cleanup
SERVER_PID=""
PORT=8000
VENV_DIR=".venv"
PROJECT_DIR="mysite"

# Cleanup function
cleanup() {
    log "Initiating shutdown procedure..."
    
    # Kill Django server process if running
    if [ -n "$SERVER_PID" ]; then
        log "Stopping Django server (PID: $SERVER_PID)"
        kill -TERM $SERVER_PID 2>/dev/null || true
        
        # Wait for process to terminate
        for i in {1..5}; do
            if ! ps -p $SERVER_PID > /dev/null 2>&1; then
                break
            fi
            log "Waiting for server to terminate... ($i/5)"
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $SERVER_PID > /dev/null 2>&1; then
            log "Server still running, forcing termination"
            kill -9 $SERVER_PID 2>/dev/null || true
        fi
    fi
    
    # Check if port is still in use
    if netstat -tuln | grep ":$PORT " > /dev/null 2>&1; then
        log "Warning: Port $PORT is still in use. Attempting to free it..."
        # Find process using the port and kill it
        pid=$(lsof -t -i:$PORT 2>/dev/null || true)
        if [ -n "$pid" ]; then
            log "Killing process $pid that's using port $PORT"
            kill -9 $pid 2>/dev/null || true
        fi
    fi
    
    # Deactivate virtual environment if active
    if [ -n "$VIRTUAL_ENV" ]; then
        log "Deactivating virtual environment"
        deactivate 2>/dev/null || true
    fi
    
    log "Cleanup complete"
    log "Server shutdown complete"
}

# Check if script is running in a virtual environment
is_in_virtualenv() {
    if [ -z "$VIRTUAL_ENV" ]; then
        return 1  # Not in a virtual environment
    else
        return 0  # In a virtual environment
    fi
}

# Set up trap for cleanup on script exit
trap cleanup EXIT INT TERM

log "Starting IntelliShop setup"

# Configuration
REQUIREMENTS_FILE="requirements.txt"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    error "Python3 is not installed or not in PATH"
fi

# If we're already in a virtual environment but not our target one, warn and deactivate
if is_in_virtualenv && [[ "$VIRTUAL_ENV" != *"$VENV_DIR"* ]]; then
    log "Warning: Already in a different virtual environment. Deactivating."
    deactivate 2>/dev/null || true
fi

# Setup or verify virtual environment
if [ -d "$VENV_DIR" ]; then
    log "Virtual environment directory exists, activating"
    source $VENV_DIR/bin/activate || error "Failed to activate existing virtual environment"
    
    # Double-check activation succeeded
    if ! is_in_virtualenv; then
        log "Virtual environment activation failed. Recreating environment."
        rm -rf $VENV_DIR
        python3 -m venv $VENV_DIR || error "Failed to create virtual environment"
        source $VENV_DIR/bin/activate || error "Failed to activate new virtual environment"
    fi
else
    log "Creating new virtual environment"
    python3 -m venv $VENV_DIR || error "Failed to create virtual environment"
    source $VENV_DIR/bin/activate || error "Failed to activate new virtual environment"
fi

# Verify we're now in a virtual environment
if ! is_in_virtualenv; then
    error "Failed to properly activate virtual environment"
fi

log "Successfully activated virtual environment: $VIRTUAL_ENV"

# Update pip to latest version
log "Updating pip to latest version"
python -m pip install --upgrade pip || log "Warning: Failed to upgrade pip"

# Install dependencies from requirements file if it exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    log "Installing dependencies from $REQUIREMENTS_FILE"
    python -m pip install -r $REQUIREMENTS_FILE || error "Failed to install requirements"
else
    # Install Django if not already installed
    if ! python -m pip show django &> /dev/null; then
        log "Installing Django"
        python -m pip install django || error "Failed to install Django"
    else
        log "Django already installed in virtual environment"
    fi
fi

# Change to the Django project directory
if [ ! -d "$PROJECT_DIR" ]; then
    error "Django project directory '$PROJECT_DIR' not found"
fi

cd $PROJECT_DIR || error "Failed to change to project directory"

# Check if port is already in use
if netstat -tuln | grep ":$PORT " > /dev/null 2>&1; then
    log "Warning: Port $PORT is already in use"
    pid=$(lsof -t -i:$PORT 2>/dev/null || true)
    if [ -n "$pid" ]; then
        log "Process $pid is using port $PORT"
        read -p "Do you want to kill this process and free the port? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log "Killing process $pid"
            kill -9 $pid || log "Failed to kill process $pid"
            sleep 2
        else
            error "Port $PORT is in use. Please free the port or use a different one."
        fi
    fi
fi

# Run database migrations if needed
log "Running database migrations"
python manage.py migrate || log "Warning: Database migration failed"

# Collect static files for production
log "Collecting static files"
python manage.py collectstatic --noinput || log "Warning: Static file collection failed"

# Check for Django configuration errors
log "Checking for configuration errors"
python manage.py check --deploy || log "Warning: Django deployment checks failed"

# Start the Django development server
log "Please wait for Django to start on port $PORT"

# Run Django server in background so we can capture its PID
python manage.py runserver 0.0.0.0:$PORT &
SERVER_PID=$!

log "Server running with PID: $SERVER_PID"

# Wait for the Django server to exit
wait $SERVER_PID 2>/dev/null || true

# The cleanup function will be called automatically through the trap 