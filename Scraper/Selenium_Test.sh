#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set the directory for the tests
TEST_DIR="$SCRIPT_DIR/pages/tests/jemix"
VENV_DIR="$SCRIPT_DIR/venv"

# Check for required browser
if [ -f /etc/debian_version ]; then
    # WSL environment
    if ! command -v chromium-browser &> /dev/null && ! command -v google-chrome &> /dev/null; then
        echo "Error: Neither Chromium nor Google Chrome is installed."
        echo "Please install either browser using your system package manager:"
        echo "sudo apt update && sudo apt install -y chromium-browser"
        exit 1
    fi
fi

# Set PYTHONPATH to include the project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Create and activate a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages
pip install selenium webdriver-manager

# Run the test module directly with increased verbosity
cd "$PROJECT_ROOT"
echo "Running tests from directory: $PWD"
python3 -m unittest Scraper.pages.tests.jemix.HomePage_load Scraper.pages.tests.jemix.LoginPage_test -v

# Store the test result
TEST_RESULT=$?

# Deactivate virtual environment
deactivate

# Exit with the test result
exit $TEST_RESULT
