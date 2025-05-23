#!/bin/bash

# Set the directory for the tests
TEST_DIR="Scraper/pages/tests/jemix"
VENV_DIR="venv"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Create and activate a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Verify pip installation in the virtual environment
if ! command_exists pip; then
    echo "pip is not installed in the virtual environment. Installing..."
    python3 -m ensurepip
fi

# Verify Selenium installation
if ! python3 -c "import selenium" &> /dev/null; then
    echo "Selenium is not installed in the virtual environment. Installing..."
    pip install selenium
fi

# Verify WebDriver installation (e.g., ChromeDriver)
if ! command_exists chromedriver; then
    echo "ChromeDriver is not installed. Installing using apt..."
    sudo apt update
    sudo apt install -y chromium-chromedriver
    if ! command_exists chromedriver; then
        echo "Failed to install ChromeDriver. Please ensure your package manager is configured correctly."
        deactivate
        exit 1
    fi
fi

# Run tests
if [ "$#" -eq 0 ]; then
    # No arguments, run all tests
    echo "Running all tests in $TEST_DIR"
    python3 -m unittest discover -s "$TEST_DIR" -p "*.py"
else
    # Run specified tests
    for test in "$@"; do
        echo "Running test: $test"
        python3 -m unittest "$TEST_DIR/$test"
    done
fi

# Deactivate the virtual environment
deactivate
