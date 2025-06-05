#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set the directories for the tests
SELENIUM_TEST_DIR="$SCRIPT_DIR/pages/tests/jemix"
API_TEST_DIR="$SCRIPT_DIR/pages/tests/potter_api"
VENV_DIR="$SCRIPT_DIR/venv"

# Check if a parameter was provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a parameter (0 for Selenium tests, 1 for API tests)"
    exit 1
fi

# Check for required browser if running Selenium tests
if [ "$1" = "0" ] && [ -f /etc/debian_version ]; then
    # WSL environment
    if ! command -v chromium-browser &> /dev/null && ! command -v google-chrome &> /dev/null; then
        echo "Error: Neither Chromium nor Google Chrome is installed."
        echo "Please install either browser using your system package manager:"
        echo "sudo apt update && sudo apt install -y chromium-browser"
        exit 1
    fi
fi

# Set PYTHONPATH to include the project root
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Create and activate a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages based on test type
if [ "$1" = "0" ]; then
    pip install selenium webdriver-manager colorama
elif [ "$1" = "1" ]; then
    pip install requests
else
    echo "Error: Invalid parameter. Use 0 for Selenium tests or 1 for API tests."
    exit 1
fi

# Create necessary directories and __init__.py files
mkdir -p "$PROJECT_ROOT/Scraper/pages/tests/jemix"
mkdir -p "$PROJECT_ROOT/Scraper/pages/tests/potter_api"
touch "$PROJECT_ROOT/Scraper/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/tests/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/tests/jemix/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/tests/potter_api/__init__.py"

# Run tests based on parameter
cd "$PROJECT_ROOT"
echo "Running tests..."

if [ "$1" = "0" ]; then
    # Run Selenium tests
    python3 "$SELENIUM_TEST_DIR/execute_tests.py"
elif [ "$1" = "1" ]; then
    # Run API tests
    python3 "$API_TEST_DIR/execute_tests.py"
fi

# Store the test result
TEST_RESULT=$?

# Deactivate virtual environment
deactivate

# Exit with the test result
exit $TEST_RESULT
