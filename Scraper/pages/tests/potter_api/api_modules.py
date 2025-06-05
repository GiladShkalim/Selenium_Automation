"""
API modules for Harry Potter Books API testing.

This module contains configuration, data models, and validation logic
for testing the Harry Potter Books API. It follows best practices for
API testing and implements reusable components.

Components:
    - APIConfig: Configuration settings for the API
    - BookSchema: Schema definition and validation for book objects
    - BookData: Known book data for validation
"""

from typing import Dict, List

class APIConfig:
    """Configuration settings for the Harry Potter API."""
    
    BASE_URL = "https://potterapi-fedeperin.vercel.app/en"
    BOOKS_ENDPOINT = "/books"
    HOUSES_ENDPOINT = "/houses"
    
    @classmethod
    def get_books_url(cls) -> str:
        """Get the full URL for the books endpoint."""
        return f"{cls.BASE_URL}{cls.BOOKS_ENDPOINT}"
    
    @classmethod
    def get_houses_url(cls) -> str:
        """Get the full URL for the houses endpoint."""
        return f"{cls.BASE_URL}{cls.HOUSES_ENDPOINT}"
    
    @classmethod
    def get_houses_url_with_params(cls, **params) -> str:
        """Get the houses URL with query parameters."""
        base_url = cls.get_houses_url()
        query_params = []
        
        for key, value in params.items():
            if value is not None:
                query_params.append(f"{key}={value}")
        
        if query_params:
            return f"{base_url}?{'&'.join(query_params)}"
        return base_url

class BookSchema:
    """Schema definition and validation for book objects."""
    
    # Required fields and their expected types
    REQUIRED_FIELDS = {
        "number": int,
        "title": str,
        "originalTitle": str,
        "releaseDate": str,
        "description": str,
        "pages": int,
        "cover": str,
        "index": int
    }
    
    @classmethod
    def validate(cls, book: Dict) -> List[str]:
        """
        Validate a book object against the schema.
        
        Args:
            book: Dictionary containing book data
            
        Returns:
            List of validation error messages (empty if validation passes)
        """
        errors = []
        
        # Check for required fields and their types
        for field, expected_type in cls.REQUIRED_FIELDS.items():
            if field not in book:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(book[field], expected_type):
                errors.append(
                    f"Invalid type for {field}: expected {expected_type.__name__}, "
                    f"got {type(book[field]).__name__}"
                )
        
        # Validate number range (1-8 for Harry Potter books)
        if "number" in book and (book["number"] < 1 or book["number"] > 8):
            errors.append(
                f"Invalid book number: {book['number']} (should be between 1 and 8)"
            )
        
        # Validate index range (0-7 for zero-based indexing)
        if "index" in book and (book["index"] < 0 or book["index"] > 7):
            errors.append(
                f"Invalid index: {book['index']} (should be between 0 and 7)"
            )
        
        # Validate cover URL format
        if "cover" in book and not book["cover"].startswith("https://"):
            errors.append(f"Invalid cover URL format: {book['cover']}")
        
        return errors

class BookData:
    """Known book data for validation testing."""
    
    # Sample of known books with verified data
    KNOWN_BOOKS = {
        1: {
            "title": "Harry Potter and the Sorcerer's Stone",
            "releaseDate": "Jun 26, 1997",
            "pages": 223
        },
        7: {
            "title": "Harry Potter and the Deathly Hallows",
            "releaseDate": "Jul 21, 2007",
            "pages": 607
        }
    }
    
    @classmethod
    def get_known_book_data(cls, book_number: int) -> Dict:
        """
        Get known data for a specific book.
        
        Args:
            book_number: The book number to get data for
            
        Returns:
            Dictionary containing known book data
        
        Raises:
            KeyError: If book_number is not found in known data
        """
        if book_number not in cls.KNOWN_BOOKS:
            raise KeyError(f"No known data for book number {book_number}")
        return cls.KNOWN_BOOKS[book_number]
    
    @classmethod
    def get_all_known_books(cls) -> Dict:
        """Get all known book data."""
        return cls.KNOWN_BOOKS.copy()

class HousesConfig:
    """Configuration settings for the Harry Potter Houses API."""
    
    HOUSES_ENDPOINT = "/houses"
    
    @classmethod
    def get_houses_url(cls) -> str:
        """Get the full URL for the houses endpoint."""
        return f"{APIConfig.BASE_URL}{cls.HOUSES_ENDPOINT}"
    
    @classmethod
    def get_houses_url_with_params(cls, **params) -> str:
        """
        Get the houses URL with query parameters.
        
        Args:
            **params: Query parameters (index, max, page, search)
        """
        base_url = cls.get_houses_url()
        query_params = []
        
        for key, value in params.items():
            if value is not None:
                query_params.append(f"{key}={value}")
        
        if query_params:
            return f"{base_url}?{'&'.join(query_params)}"
        return base_url

class HouseSchema:
    """Schema definition for house objects."""
    
    REQUIRED_FIELDS = {
        "house": str,
        "emoji": str,
        "founder": str,
        "colors": list,
        "animal": str,
        "index": int
    }
    
    KNOWN_HOUSES = {
        "Gryffindor": {"index": 0, "animal": "Lion", "emoji": "🦁"},
        "Hufflepuff": {"index": 1, "animal": "Badger", "emoji": "🦡"},
        "Ravenclaw": {"index": 2, "animal": "Raven", "emoji": "🦅"},
        "Slytherin": {"index": 3, "animal": "Snake", "emoji": "🐍"}
    } 