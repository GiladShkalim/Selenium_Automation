"""
Test module for Harry Potter Houses API.

This module focuses on testing different aspects of the Houses API endpoint:
1. Query Parameter Testing
2. Response Filtering
3. Search Functionality
4. Pagination Testing
5. Error Handling

Different from the books API tests, this module emphasizes:
- Dynamic query parameter handling
- Search functionality testing
- Pagination and filtering
- Error scenarios and edge cases
"""

import unittest
import requests
import json
from typing import Dict, List, Optional
from urllib.parse import quote

from .api_modules import APIConfig, HousesConfig, HouseSchema

class TestHarryPotterHousesAPI(unittest.TestCase):
    """Test suite for Harry Potter Houses API endpoint."""
    
    @classmethod
    def setUpClass(cls):
        """Class-level setup - runs once before all tests."""
        cls.session = requests.Session()
        cls.base_url = HousesConfig.get_houses_url()
    
    def test_query_parameter_combinations(self):
        """
        Test various combinations of query parameters.
        Tests the API's ability to handle multiple parameters simultaneously.
        """
        test_cases = [
            {"index": 0},
            {"max": 2},
            {"max": 2, "page": 1},
            {"search": "Gryffindor"},
            {"max": 2, "search": "Sly"}
        ]
        
        for params in test_cases:
            with self.subTest(params=params):
                url = HousesConfig.get_houses_url_with_params(**params)
                response = self.session.get(url)
                
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Failed with params {params}: {response.text}"
                )
                
                data = response.json()
                
                if "index" in params:
                    self.assertEqual(
                        len(data),
                        1,
                        "Single index query should return one house"
                    )
                    self.assertEqual(
                        data[0]["index"],
                        params["index"],
                        "Returned house index should match query"
                    )
                
                if "max" in params:
                    self.assertLessEqual(
                        len(data),
                        params["max"],
                        f"Response should not exceed max={params['max']}"
                    )
    
    def test_search_functionality(self):
        """
        Test the search feature with various search terms.
        Focuses on search accuracy and partial matches.
        """
        search_tests = [
            ("Gryff", "Gryffindor"),  # Partial name
            ("Snake", "Slytherin"),    # Animal match
            ("Helga", "Hufflepuff"),   # Founder name
            ("blue", "Ravenclaw")      # Color match
        ]
        
        for search_term, expected_house in search_tests:
            with self.subTest(search_term=search_term):
                url = HousesConfig.get_houses_url_with_params(search=search_term)
                response = self.session.get(url)
                
                self.assertEqual(response.status_code, 200)
                data = response.json()
                
                # Verify the expected house is in the results
                house_names = [house["house"] for house in data]
                self.assertIn(
                    expected_house,
                    house_names,
                    f"Search for '{search_term}' should return {expected_house}"
                )
    
    def test_pagination_consistency(self):
        """
        Test pagination consistency and completeness.
        Ensures no data is lost or duplicated across pages.
        """
        page_size = 2
        all_houses = set()
        
        # Collect houses across all pages
        for page in range(2):  # 4 houses ÷ 2 per page = 2 pages
            url = HousesConfig.get_houses_url_with_params(max=page_size, page=page)
            response = self.session.get(url)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            # Collect house names from this page
            page_houses = {house["house"] for house in data}
            
            # Ensure no duplicates
            self.assertEqual(
                len(page_houses.intersection(all_houses)),
                0,
                "Found duplicate houses across pages"
            )
            
            all_houses.update(page_houses)
        
        # Verify we got all houses
        self.assertEqual(
            len(all_houses),
            4,
            "Pagination should return all houses exactly once"
        )
    
    def test_error_handling(self):
        """
        Test error handling for invalid parameters.
        Focuses on API's error responses and edge cases.
        """
        error_cases = [
            {"index": 99},           # Invalid index
            {"max": -1},             # Invalid max
            {"page": 999},           # Invalid page
            {"max": "invalid"},      # Invalid type
            {"search": ""}           # Empty search
        ]
        
        for params in error_cases:
            with self.subTest(params=params):
                url = HousesConfig.get_houses_url_with_params(**params)
                response = self.session.get(url)
                
                if "index" in params and params["index"] >= 4:
                    self.assertEqual(
                        response.status_code,
                        404,
                        "Should return 404 for invalid index"
                    )
                    self.assertIn(
                        "error",
                        response.json(),
                        "Error response should contain error message"
                    )
    
    def test_response_headers(self):
        """
        Test response headers and caching behavior.
        Focuses on API's caching and content type headers.
        """
        response = self.session.get(self.base_url)
        
        # Verify content type
        self.assertIn(
            'application/json',
            response.headers['Content-Type'].lower(),
            "Response should be JSON"
        )
        
        # Verify cache control
        self.assertIn(
            'cache-control',
            response.headers,
            "Response should include cache control header"
        )
        
        # Verify specific cache directives
        cache_control = response.headers['cache-control'].lower()
        self.assertIn('public', cache_control)
        self.assertIn('must-revalidate', cache_control)
    
    def tearDown(self):
        """Method-level cleanup - runs after each test method."""
        pass
    
    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup - runs once after all tests."""
        if hasattr(cls, 'session'):
            cls.session.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
