#!/bin/bash

# IntelliShop Project Runner
# This script sets up and runs the IntelliShop web application
#
# === USAGE INSTRUCTIONS ===
# How to run:
#   1. Make this script executable: chmod +x build.sh
#   2. Run the script in WSL terminal: ./build.sh [1]
#      - Add "1" parameter to update the database with sample data
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
ENV_FILE=".env"
ABSOLUTE_ENV_FILE="$(pwd)/$ENV_FILE"  # Store absolute path to .env file

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

# MongoDB configuration setup
setup_mongodb_config() {
    log "Setting up MongoDB configuration..."
    # Create .env file if it doesn't exist
    if [ ! -f "$ENV_FILE" ]; then
        log "Creating environment configuration file..."
        cat > "$ENV_FILE" << EOF
# MongoDB Configuration
MONGODB_URI=
MONGODB_NAME=IntelliDB

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
EOF
        log "Created environment template at $ENV_FILE"
        log "⚠️  IMPORTANT: Please edit $ENV_FILE with your actual MongoDB credentials"
    else
        log "Environment file $ENV_FILE already exists"
    fi
    
    # Load environment variables
    log "Loading configuration from $ENV_FILE"
    if [ -f "$ENV_FILE" ]; then
        # Export environment variables properly - only export valid variable assignments
        while IFS= read -r line || [ -n "$line" ]; do
            # Skip comments and empty lines
            if [[ $line =~ ^[[:space:]]*# || -z $line ]]; then
                continue
            fi
            
            # Only export if line contains a valid KEY=VALUE format (no spaces around =)
            if [[ $line =~ ^[A-Za-z0-9_]+=.* ]]; then
                export "$line" || log "Warning: Failed to export environment variable: $line"
            else
                log "Warning: Skipping invalid environment variable: $line"
            fi
        done < "$ENV_FILE"
    else
        log "⚠️  $ENV_FILE file not found. MongoDB connection may fail."
    fi
}

# Test MongoDB connection
test_mongodb_connection() {
    log "Testing MongoDB connection..."
    
    # Check if MongoDB URI is set
    if [ -z "$MONGODB_URI" ]; then
        log "⚠️  MongoDB URI not set. Skipping connection test."
        return 1
    fi
    
    # Simple test script
    python3 -c "
from pymongo import MongoClient
import os
import sys

try:
    uri = os.environ.get('MONGODB_URI')
    if not uri:
        print('MongoDB URI not found in environment variables')
        sys.exit(1)
    
    client = MongoClient(uri)
    info = client.server_info()
    print(f'Successfully connected to MongoDB v{info.get(\"version\")}')
    sys.exit(0)
except Exception as e:
    print(f'MongoDB connection error: {e}')
    sys.exit(1)
" && return 0 || return 1
}

# Create necessary MongoDB files
create_mongodb_files() {
    log "Creating MongoDB utility files..."
    
    # Create directories if they don't exist
    mkdir -p "$PROJECT_DIR/intellishop/utils"
    mkdir -p "$PROJECT_DIR/intellishop/models"
    mkdir -p "$PROJECT_DIR/intellishop/management/commands"
    
    # Create mongodb_utils.py
    local MONGODB_UTILS_FILE="$PROJECT_DIR/intellishop/utils/mongodb_utils.py"
    if [ ! -f "$MONGODB_UTILS_FILE" ]; then
        log "Creating MongoDB utility file..."
        cat > "$MONGODB_UTILS_FILE" << 'EOF'
from pymongo import MongoClient
import os

def get_db_handle():
    """
    Returns a handle to the MongoDB database and client
    """
    # Get MongoDB connection details from environment variables or settings
    mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
    db_name = os.environ.get('MONGODB_NAME', 'intellishop_db')
    
    # Create a MongoDB client
    client = MongoClient(mongodb_uri)
    db_handle = client[db_name]
    
    return db_handle, client

def get_collection_handle(collection_name):
    """
    Returns a handle to a specific MongoDB collection
    """
    db, client = get_db_handle()
    return db[collection_name]
EOF
        log "Created MongoDB utility file at $MONGODB_UTILS_FILE"
    else
        log "MongoDB utility file already exists"
    fi
    
    # Create __init__.py files to make directories into packages
    touch "$PROJECT_DIR/intellishop/utils/__init__.py"
    touch "$PROJECT_DIR/intellishop/models/__init__.py"
    
    # Create mongodb_models.py
    local MONGODB_MODELS_FILE="$PROJECT_DIR/intellishop/models/mongodb_models.py"
    if [ ! -f "$MONGODB_MODELS_FILE" ]; then
        log "Creating MongoDB models file..."
        cat > "$MONGODB_MODELS_FILE" << 'EOF'
from bson import ObjectId

class MongoDBModel:
    """Base class for MongoDB models"""
    collection_name = None
    
    @classmethod
    def get_collection(cls):
        """Get the MongoDB collection for this model"""
        from intellishop.utils.mongodb_utils import get_collection_handle
        return get_collection_handle(cls.collection_name)
    
    @classmethod
    def find_one(cls, query):
        """Find a single document"""
        return cls.get_collection().find_one(query)
    
    @classmethod
    def find(cls, query=None, sort=None, limit=None):
        """Find multiple documents"""
        cursor = cls.get_collection().find(query or {})
        
        if sort:
            cursor = cursor.sort(sort)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    @classmethod
    def insert_one(cls, document):
        """Insert a document into the collection"""
        result = cls.get_collection().insert_one(document)
        return result.inserted_id
    
    @classmethod
    def update_one(cls, query, update):
        """Update a document in the collection"""
        return cls.get_collection().update_one(query, {'$set': update})
    
    @classmethod
    def delete_one(cls, query):
        """Delete a document from the collection"""
        return cls.get_collection().delete_one(query)
EOF
        log "Created MongoDB models file at $MONGODB_MODELS_FILE"
    else
        log "MongoDB models file already exists"
    fi
    
    # Create test command
    mkdir -p "$PROJECT_DIR/intellishop/management/commands"
    touch "$PROJECT_DIR/intellishop/management/__init__.py"
    touch "$PROJECT_DIR/intellishop/management/commands/__init__.py"
    
    local TEST_COMMAND_FILE="$PROJECT_DIR/intellishop/management/commands/test_mongodb.py"
    if [ ! -f "$TEST_COMMAND_FILE" ]; then
        log "Creating MongoDB test command..."
        cat > "$TEST_COMMAND_FILE" << 'EOF'
from django.core.management.base import BaseCommand
from intellishop.utils.mongodb_utils import get_db_handle

class Command(BaseCommand):
    help = 'Test MongoDB connection'

    def handle(self, *args, **options):
        try:
            db, client = get_db_handle()
            server_info = client.server_info()
            self.stdout.write(self.style.SUCCESS(f'Successfully connected to MongoDB version: {server_info["version"]}'))
            self.stdout.write(self.style.SUCCESS(f'Available databases: {client.list_database_names()}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to MongoDB: {e}'))
        finally:
            if 'client' in locals():
                client.close()
EOF
        log "Created MongoDB test command at $TEST_COMMAND_FILE"
    else
        log "MongoDB test command already exists"
    fi
}

# Groq API Enhancement Functions
verify_api_key() {
    log "Verifying Groq API key..."
    
    # Check if .env file exists
    if [ ! -f "$ABSOLUTE_ENV_FILE" ]; then
        log "❌ $ABSOLUTE_ENV_FILE file not found."
        log "Creating template .env file..."
        
        # Create template .env file
        cat > "$ABSOLUTE_ENV_FILE" << EOF
GROQ_API_KEY=your_api_key_here
EOF
        
        error "Please update the .env file with your actual Groq API key and run again."
    fi
    
    # Load and check API key
    source "$ABSOLUTE_ENV_FILE" 2>/dev/null
    
    if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_api_key_here" ]; then
        error "Invalid or missing Groq API key in $ABSOLUTE_ENV_FILE. Please update it."
    fi
    
    log "✅ Groq API key found."
}

validate_script() {
    local SCRIPT_FILE="$1"
    
    if [ ! -f "$SCRIPT_FILE" ]; then
        error "Script file $SCRIPT_FILE not found in $(pwd). Please check the file path."
    fi
    
    log "✅ Script validation passed."
}

run_enhancement_process() {
    local SCRIPT_FILE="$1"
    
    # Run the script
    log "Starting data enhancement process..."

    python "$SCRIPT_FILE" &
    local ENHANCEMENT_PID=$!

    log "Process running with PID: $ENHANCEMENT_PID"

    # Wait for the script to complete
    wait $ENHANCEMENT_PID 2>/dev/null
    local EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        log "✅ Enhancement process completed successfully!"
        log "Enhanced files have been saved in the data directory."
    else
        log "❌ Enhancement process failed with exit code $EXIT_CODE."
    fi
}

# Set up trap for cleanup on script exit
trap cleanup EXIT INT TERM

echo "Checking Python version..."

# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python 3 detected: $PYTHON_VERSION"
else
    echo "❌ Python 3 not detected. Installing Python 3..."
    
    # Detect OS and install Python
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Detected macOS. Using Homebrew to install Python 3..."
        if command -v brew &>/dev/null; then
            brew install python3
        else
            echo "Homebrew not installed. Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install python3
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Detected Linux. Installing Python 3..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v yum &>/dev/null; then
            sudo yum install -y python3 python3-pip
        else
            echo "ERROR: Unsupported package manager. Please install Python 3 manually."
            exit 1
        fi
    else
        echo "ERROR: Unsupported operating system. Please install Python 3 manually."
        exit 1
    fi
    
    # Verify Python was installed
    if command -v python3 &>/dev/null; then
        PYTHON_VERSION=$(python3 --version)
        echo "✅ Python 3 installed successfully: $PYTHON_VERSION"
    else
        echo "❌ Failed to install Python 3. Please install manually."
        exit 1
    fi
fi

log "Starting IntelliShop setup"

# Configuration
REQUIREMENTS_FILE="requirements.txt"

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

# Loading spinner function
show_spinner() {
    local pid=$1
    local message=$2
    local spin='-\|/'
    local i=0
    
    # Save cursor position and hide cursor
    tput sc
    tput civis
    
    echo -n "$message "
    
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 4 ))
        printf "\r$message ${spin:$i:1}"
        sleep 0.1
    done
    
    # Clear line, restore cursor position and show cursor
    printf "\r\033[K$message Complete!"
    echo
    tput cnorm
}

# Progress bar function
show_progress_bar() {
    local pid=$1
    local message=$2
    local width=40
    
    # Save cursor position and hide cursor
    tput sc
    tput civis
    
    echo -n "$message "
    
    local i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % (width+1) ))
        # Create the progress bar
        printf "\r$message ["
        printf "%${i}s" | tr ' ' '='
        printf "%$(( width - i ))s" | tr ' ' ' '
        printf "] %d%%" $(( (i * 100) / width ))
        sleep 0.1
    done
    
    # Show completed progress bar
    printf "\r$message ["
    printf "%${width}s" | tr ' ' '='
    printf "] 100%%"
    echo
    tput cnorm
}

# Update pip to latest version
log "Updating pip to latest version"
python -m pip install --upgrade pip > /dev/null 2>&1 &
PIP_PID=$!
show_progress_bar $PIP_PID "Updating pip"
wait $PIP_PID
if [ $? -ne 0 ]; then
    log "Warning: Failed to upgrade pip"
fi

# Install dependencies from requirements file if it exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    log "Installing dependencies from $REQUIREMENTS_FILE"
    python -m pip install -r $REQUIREMENTS_FILE > /dev/null 2>&1 &
    PIP_PID=$!
    show_progress_bar $PIP_PID "Installing dependencies"
    wait $PIP_PID
    if [ $? -ne 0 ]; then
        error "Failed to install requirements"
    fi
else
    # Install Django if not already installed
    if ! python -m pip show django &> /dev/null; then
        log "Installing Django"
        python -m pip install django > /dev/null 2>&1 &
        PIP_PID=$!
        show_progress_bar $PIP_PID "Installing Django"
        wait $PIP_PID
        if [ $? -ne 0 ]; then
            error "Failed to install Django"
        fi
    else
        log "Django already installed in virtual environment"
    fi
    
    # Install MongoDB dependencies
    log "Installing PyMongo and dnspython"
    python -m pip install pymongo dnspython > /dev/null 2>&1 &
    PIP_PID=$!
    show_progress_bar $PIP_PID "Installing MongoDB dependencies"
    wait $PIP_PID
    if [ $? -ne 0 ]; then
        log "Warning: Failed to install MongoDB dependencies"
    fi
fi

# Set up MongoDB configuration
setup_mongodb_config

# Create MongoDB utility files
create_mongodb_files

# Change to the Django project directory
if [ ! -d "$PROJECT_DIR" ]; then
    error "Django project directory '$PROJECT_DIR' not found"
fi

cd $PROJECT_DIR || error "Failed to change to project directory"

# Test MongoDB connection
test_mongodb_connection || log "Warning: MongoDB connection test failed. The application may not function correctly."

# Run database migrations if needed
log "Running database migrations"
python manage.py migrate || log "Warning: Database migration failed"

# Collect static files for production
log "Collecting static files"
python manage.py collectstatic --noinput || log "Warning: Static file collection failed"

# Check for Django configuration errors
log "Checking for configuration errors"
python manage.py check --deploy || log "Warning: Django deployment checks failed"

# Check if database update was requested
if [ "$1" = "1" ]; then
    log "Database update requested. Running update script..."
    python update_database.py
    if [ $? -ne 0 ]; then
        log "⚠️ Database update failed!"
    else
        log "✅ Database updated successfully!"
    fi
elif [ "$1" = "2" ]; then
    # Define Groq-specific variables
    GROQ_SCRIPT_FILE="groq_chat.py"
    GROQ_REQUIREMENTS_FILE="requirements.txt"
    
    log "Running AI enhancement process..."
    
    # Verify the Groq API key
    verify_api_key
    
    # Validate script files
    validate_script "$GROQ_SCRIPT_FILE" "$GROQ_REQUIREMENTS_FILE"
    
    # Run the enhancement process
    run_enhancement_process "$GROQ_SCRIPT_FILE"
    
    # Then run the database update script
    log "Running database update script..."
    python update_database.py
    if [ $? -ne 0 ]; then
        log "⚠️ Database update failed!"
    else
        log "✅ Database updated successfully!"
    fi
else
    log "Skipping database update. Run with './build.sh 1' to update the database or './build.sh 2' for AI enhancement and database update."
fi

SERVER_PID=$!

log "Server running with PID: $SERVER_PID"

# Wait for the Django server to exit
wait $SERVER_PID 2>/dev/null || true

# The cleanup function will be called automatically through the trap 
