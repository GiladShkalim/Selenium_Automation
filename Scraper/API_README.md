# Harry Potter API Testing Suite

## Overview
A testing suite for validating the Harry Potter Books and Houses API endpoints. 
Site tested URL: https://potterapi-fedeperin.vercel.app/en/books
Site tested Swagger: https://vlaurencena.github.io/harry-potter-openapi-swagger-ui/#/

## Project Structure
```
/potter_api/
├── __init__.py
├── api_get.py         # Books API test implementation
├── api_houses.py      # Houses API test implementation
├── api_modules.py     # Shared configurations and schemas
├── execute_tests.py   # Test runner and orchestrator
└── test_utils.py      # Testing utilities and result handling
```

## Core Components

### Test Modules
- **api_get.py**: Implements test cases for the Books API endpoint
- **api_houses.py**: Contains test cases for the Houses API endpoint
- **api_modules.py**: Houses shared configurations, schemas, and data models

### Test Infrastructure
- **execute_tests.py**: Main test runner that orchestrates test execution
- **test_utils.py**: Utilities for test result handling and reporting
- **API-Test-Result.txt**: Generated report containing test execution results

### Test Runner
- **Selenium_Test.sh**: Shell script for test environment setup and execution

## Key Features
- Comprehensive API endpoint testing
- Schema validation
- Data consistency checks
- Pagination testing
- Search functionality validation
- Error handling verification
- Automated test result reporting

## Prerequisites
- Python 3.x
- `requests` library
- Unix-like environment (for shell script execution)

## Installation
1. Clone the repository
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Unix/macOS
```
3. Install dependencies:
```bash
pip install requests
```

## Usage
Run the API tests using:
```bash
./Selenium_Test.sh 1
```

## Test Results
Test results are automatically generated in `API-Test-Result.txt`, containing:
- Failed test cases with detailed error messages
- Test execution summary
- Total tests count
- Pass/Fail statistics
