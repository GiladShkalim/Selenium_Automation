# Harry Potter API Test Cases Documentation

## Books API Tests (`api_get.py`)

### TestHarryPotterBooksAPI
1. **test_get_all_books**
   - Verifies successful retrieval of all books
   - Validates response status code (200)
   - Checks Content-Type header
   - Ensures response contains 8 books
   - Validates response format (JSON list)

2. **test_book_schema_validation**
   - Validates schema for each book object
   - Checks required fields presence and types
   - Verifies field constraints (e.g., book numbers 1-8)

3. **test_book_data_validation**
   - Validates specific book data against known values
   - Checks titles, release dates, and page counts
   - Verifies data consistency with canonical sources

## Houses API Tests (`api_houses.py`)

### TestHarryPotterHousesAPI
1. **test_query_parameter_combinations**
   - Tests various query parameter combinations
   - Validates index-based queries
   - Tests max results parameter
   - Verifies pagination functionality
   - Checks search parameter handling

2. **test_search_functionality**
   - Tests search with partial house names
   - Validates animal-based searches
   - Tests founder name searches
   - Verifies color-based searches
   - Ensures accurate result matching

3. **test_pagination_consistency**
   - Verifies consistent pagination behavior
   - Checks for duplicate entries across pages
   - Validates complete data retrieval
   - Tests page size constraints

4. **test_error_handling**
   - Tests invalid index values
   - Validates negative max values handling
   - Checks invalid page numbers
   - Verifies type validation
   - Tests empty search handling

5. **test_response_headers**
   - Validates Content-Type headers
   - Checks cache control directives
   - Verifies cache-related headers
   - Tests header consistency

## Shared Components (`api_modules.py`)

### Configuration Classes
- **APIConfig**: Base URL and endpoint configurations
- **BookSchema**: Book object validation schema
- **BookData**: Known book data for validation
- **HousesConfig**: Houses endpoint configuration
- **HouseSchema**: House object validation schema

## Test Infrastructure

### ResultFileWriter (`test_utils.py`)
- Manages test result file generation
- Formats test outcomes
- Handles success and failure reporting
- Generates execution summaries

### Test Runner (`execute_tests.py`)
- Orchestrates test execution
- Manages test suite composition
- Handles result collection
- Controls test verbosity levels 