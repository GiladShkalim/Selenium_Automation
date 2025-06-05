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
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Create and activate a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages
pip install selenium webdriver-manager colorama

# Create a Python script for test execution
cat > "$TEST_DIR/execute_tests.py" << 'EOL'
import unittest
import sys
from test_utils import ResultFileWriter, SilentTestRunner
from Scraper.pages.tests.jemix.HomePage_load import TestHomePageLoad
from Scraper.pages.tests.jemix.LoginPage_test import TestLogin
from Scraper.pages.tests.jemix.test_logout import TestLogout
from Scraper.pages.tests.jemix.test_main_navigation import TestMainNavigation
from Scraper.pages.tests.jemix.test_category_navigation import TestCategoryNavigation

if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test cases
    test_cases = [
        TestHomePageLoad,
        TestLogin,
        TestLogout,
        TestMainNavigation,
        TestCategoryNavigation
    ]
    
    for test_case in test_cases:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
    
    # Run tests silently
    runner = SilentTestRunner()
    result = runner.run(suite)
    
    # Write results to file
    writer = ResultFileWriter()
    writer.write_results(result)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
EOL

# Create __init__.py files if they don't exist
mkdir -p "$PROJECT_ROOT/Scraper/pages/tests/jemix"
touch "$PROJECT_ROOT/Scraper/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/tests/__init__.py"
touch "$PROJECT_ROOT/Scraper/pages/tests/jemix/__init__.py"

# Run the tests
cd "$PROJECT_ROOT"
echo "Running tests..."
python3 "$TEST_DIR/execute_tests.py"

# Store the test result
TEST_RESULT=$?

# Deactivate virtual environment
deactivate

# Exit with the test result
exit $TEST_RESULT
