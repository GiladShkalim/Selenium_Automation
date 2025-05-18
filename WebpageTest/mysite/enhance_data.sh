#!/bin/bash

# Source common utility functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"  # Common.sh is now in the same directory

# Script-specific configuration
SCRIPT_NAME="BuildScript"  # or "EnhanceScript"

# Discount Data Enhancement Script
# This script sets up and runs the Groq API discount enhancement tool
#
# === USAGE INSTRUCTIONS ===
# How to run:
#   1. Make this script executable: chmod +x enhance_data.sh
#   2. Run the script: ./enhance_data.sh
#
# How to close:
#   - Press Ctrl+C in the terminal to stop the script
# ===========================

# Global variables for cleanup
SCRIPT_PID=""
VENV_DIR="venv"
ENV_FILE=".env"
SCRIPT_FILE="groq_chat.py"
REQUIREMENTS_FILE="requirements.txt"

# Cleanup function
cleanup() {
    log "Initiating shutdown procedure..."
    
    # Kill script process if running
    if [ -n "$SCRIPT_PID" ]; then
        log "Stopping script process (PID: $SCRIPT_PID)"
        kill -TERM $SCRIPT_PID 2>/dev/null || true
    fi
    
    # Deactivate virtual environment if active
    if [ -n "$VIRTUAL_ENV" ]; then
        log "Deactivating virtual environment"
        deactivate 2>/dev/null || true
    fi
    
    log "Cleanup complete"
}

# Verify the Groq API key
verify_api_key() {
    log "Verifying Groq API key..."
    
    # Check if .env file exists
    if [ ! -f "$ENV_FILE" ]; then
        log "❌ $ENV_FILE file not found."
        log "Creating template .env file..."
        
        # Create template .env file
        cat > "$ENV_FILE" << EOF
GROQ_API_KEY=your_api_key_here
EOF
        
        error "Please update the .env file with your actual Groq API key and run again."
    fi
    
    # Load and check API key
    source "$ENV_FILE" 2>/dev/null
    
    if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_api_key_here" ]; then
        error "Invalid or missing Groq API key in $ENV_FILE. Please update it."
    fi
    
    log "✅ Groq API key found."
}

# Validate script existence
validate_script() {
    log "Validating script file..."
    
    if [ ! -f "$SCRIPT_FILE" ]; then
        error "Script file $SCRIPT_FILE not found in $(pwd). Please check the file path."
    fi
    
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        error "Requirements file $REQUIREMENTS_FILE not found in $(pwd). Please check the file path."
    fi
    
    log "✅ Script validation passed."
}

# Set up trap for cleanup on script exit
trap cleanup EXIT INT TERM

log "Starting Discount Data Enhancement Tool"

# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    log "✅ Python 3 detected: $PYTHON_VERSION"
else
    log "❌ Python 3 not detected. Installing Python 3..."
    
    # Detect OS and install Python
    if command -v apt-get &>/dev/null; then
        log "Detected Debian/Ubuntu. Installing Python 3..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &>/dev/null; then
        log "Detected Red Hat/CentOS. Installing Python 3..."
        sudo yum install -y python3 python3-pip
    else
        error "Unsupported package manager. Please install Python 3 manually."
    fi
    
    # Verify Python was installed
    if command -v python3 &>/dev/null; then
        PYTHON_VERSION=$(python3 --version)
        log "✅ Python 3 installed successfully: $PYTHON_VERSION"
    else
        error "Failed to install Python 3. Please install manually."
    fi
fi

# Setup or verify virtual environment
setup_virtual_environment $VENV_DIR

# Update pip to latest version with progress bar
log "Updating pip to latest version"
python -m pip install --upgrade pip > /dev/null 2>&1 &
PIP_PID=$!
show_progress_bar $PIP_PID "Installing pip..."
if wait $PIP_PID; then
    log "✅ Pip updated successfully"
else
    log "⚠️ Warning: Failed to upgrade pip"
fi

# Install dependencies from requirements file with progress bar
if [ -f "$REQUIREMENTS_FILE" ]; then
    log "Installing dependencies from $REQUIREMENTS_FILE"
    python -m pip install -r $REQUIREMENTS_FILE > /dev/null 2>&1 &
    DEP_PID=$!
    show_progress_bar $DEP_PID "Installing dependencies..."
    if wait $DEP_PID; then
        log "✅ Dependencies installed successfully"
    else
        error "Failed to install requirements"
    fi
else
    error "Requirements file $REQUIREMENTS_FILE not found."
fi

# Verify the Groq API key
verify_api_key

# Validate script
validate_script

# Run the script
log "Starting data enhancement process..."

python "$SCRIPT_FILE" &
SCRIPT_PID=$!

log "Process running with PID: $SCRIPT_PID"

# Wait for the script to complete
wait $SCRIPT_PID 2>/dev/null
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    log "✅ Enhancement process completed successfully!"
    
    # We can't check for specific files anymore, so just report success
    log "Enhanced files have been saved in the data directory."
else
    log "❌ Enhancement process failed with exit code $EXIT_CODE."
fi

# The cleanup function will be called automatically through the trap
log "Script execution completed."
