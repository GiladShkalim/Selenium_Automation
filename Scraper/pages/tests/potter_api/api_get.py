"""
Test module for Harry Potter Books API.

This module contains test cases for verifying the GET endpoints of the Harry Potter Books API.
It follows best practices for API testing and implements comprehensive validation of responses.

Test Cases:
    - test_get_all_books: Verifies successful retrieval of all books
    - test_book_schema_validation: Validates the schema of book objects
    - test_book_data_validation: Validates specific book data against known values
"""

import unittest
import requests
import json
from typing import Dict, List

from Scraper.pages.tests.potter_api.api_modules import APIConfig, BookSchema, BookData

class TestHarryPotterBooksAPI(unittest.TestCase):
    """Test suite for Harry Potter Books API endpoints."""
    
    @classmethod
    def setUpClass(cls):
        """Class-level setup - runs once before all tests."""
        cls.session = requests.Session()
        cls.api_url = APIConfig.get_books_url()
    
    def setUp(self):
        """Method-level setup - runs before each test method."""
        self.response = None
        self.books_data = None
    
    def test_get_all_books(self):
        """Test retrieving all books from the API."""
        try:
            # Send GET request
            self.response = self.session.get(self.api_url)
            
            # Validate response status code
            self.assertEqual(
                self.response.status_code,
                200,
                f"Expected status code 200, but got {self.response.status_code}"
            )
            
            # Validate response headers
            self.assertIn(
                'application/json',
                self.response.headers['Content-Type'].lower(),
                "Response Content-Type should be application/json"
            )
            
            # Parse response body
            self.books_data = self.response.json()
            
            # Validate response is a list
            self.assertIsInstance(
                self.books_data,
                list,
                f"Expected response to be a list, but got {type(self.books_data)}"
            )
            
            # Validate number of books
            self.assertEqual(
                len(self.books_data),
                8,
                f"Expected 8 books, but got {len(self.books_data)}"
            )
            
        except requests.RequestException as e:
            self.fail(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON response: {str(e)}")
    
    def test_book_schema_validation(self):
        """Test schema validation for all book objects."""
        try:
            # Get books if not already fetched
            if not self.books_data:
                self.response = self.session.get(self.api_url)
                self.books_data = self.response.json()
            
            # Validate schema for each book
            for book in self.books_data:
                validation_errors = BookSchema.validate(book)
                
                self.assertEqual(
                    len(validation_errors),
                    0,
                    f"Schema validation failed for book {book.get('number', 'unknown')}: "
                    f"{', '.join(validation_errors)}"
                )
                
        except requests.RequestException as e:
            self.fail(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON response: {str(e)}")
    
    def test_book_data_validation(self):
        """Test specific book data against known values."""
        try:
            # Get books if not already fetched
            if not self.books_data:
                self.response = self.session.get(self.api_url)
                self.books_data = self.response.json()
            
            # Create a dictionary mapping book numbers to book data
            books_by_number = {book["number"]: book for book in self.books_data}
            
            # Validate specific books against known data
            known_books = BookData.get_all_known_books()
            for book_number, known_data in known_books.items():
                self.assertIn(
                    book_number,
                    books_by_number,
                    f"Book {book_number} not found in response"
                )
                
                book = books_by_number[book_number]
                for field, value in known_data.items():
                    self.assertEqual(
                        book[field],
                        value,
                        f"Mismatch in book {book_number} {field}: "
                        f"expected '{value}', got '{book[field]}'"
                    )
                    
        except requests.RequestException as e:
            self.fail(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON response: {str(e)}")
        except KeyError as e:
            self.fail(f"Data validation error: {str(e)}")
    
    def tearDown(self):
        """Method-level cleanup - runs after each test method."""
        self.response = None
        self.books_data = None
    
    @classmethod
    def tearDownClass(cls):
        """Class-level cleanup - runs once after all tests."""
        if hasattr(cls, 'session'):
            cls.session.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
