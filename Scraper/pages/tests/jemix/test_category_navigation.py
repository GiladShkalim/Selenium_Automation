"""
Test module for Category Navigation functionality.

This module contains test cases for verifying the navigation between different
categories and the proper loading of provider lists for each category.
"""

import unittest
import platform
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from Scraper.pages.jemix.CategoryPage import CategoryPage
from Scraper.config.settings import PAGES

class TestCategoryNavigation(unittest.TestCase):
    """Test suite for category navigation functionality."""
    
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup - runs once before all tests.
        Creates a temporary directory for Chrome user data.
        """
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
        """
        Method-level setup - runs before each test method.
        Initializes WebDriver and page objects.
        """
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Use headless mode in WSL or CI environments
            if platform.system() == "Linux" and "microsoft" in platform.uname().release.lower():
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--headless=new")

            # Initialize Chrome driver with automatic ChromeDriver management
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Initialize category pages
            self.category_pages = {}
            for page in PAGES:
                if page["name"] not in ["Home", "login", "account"]:
                    self.category_pages[page["name"]] = CategoryPage(self.driver, page["url"])
            
        except Exception as e:
            raise

    def verify_provider_list(self, category_name):
        """
        Helper method to verify provider list for a category.
        Args:
            category_name: Name of the category being tested
        Returns:
            bool: True if verification passes, False otherwise
        """
        try:
            # Wait for and verify the provider list container
            provider_list = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "elementor-posts-container"))
            )
                
            # Get all provider articles
            providers = provider_list.find_elements(By.CLASS_NAME, "elementor-post")
            total_providers = len(providers)
            valid_providers = 0
            
            # Verify each provider article
            for provider in providers:
                try:
                    # Check for thumbnail link
                    thumbnail_link = provider.find_element(By.CLASS_NAME, "elementor-post__thumbnail__link")
                    thumbnail = provider.find_element(By.CLASS_NAME, "elementor-post__thumbnail")
                    valid_providers += 1
                    
                except NoSuchElementException:
                    # Check if this is an empty article (valid case to skip)
                    try:
                        empty_text_div = provider.find_element(By.CLASS_NAME, "elementor-post__text")
                        if not empty_text_div.text.strip():  # If the text div is empty
                            continue
                    except NoSuchElementException:
                        continue
            
            # Test passes if we found at least one valid provider
            return valid_providers > 0
                
        except Exception:
            return False

    def test_category_navigation(self):
        """
        Test navigation through all categories and verify provider lists.
        Verifies:
        1. Navigation to each category page
        2. Provider list display and structure
        3. Category-specific content
        """
        for category_name, category_page in self.category_pages.items():
            try:
                # Navigate to category
                category_page.navigate_to_category()
                
                # Verify provider list
                self.assertTrue(
                    self.verify_provider_list(category_name),
                    f"Provider list verification failed for category: {category_name}"
                )
                
                # Verify category-specific elements
                current_url = self.driver.current_url
                self.assertIn(
                    category_name.lower().replace(" ", "-"),
                    current_url.lower(),
                    f"URL does not match category: {category_name}"
                )
                
            except AssertionError as ae:
                raise
            except Exception as e:
                raise

    def tearDown(self):
        """
        Method-level cleanup - runs after each test method.
        Closes the WebDriver instance.
        """
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception:
                pass

    @classmethod
    def tearDownClass(cls):
        """
        Class-level cleanup - runs once after all tests.
        Removes the temporary Chrome profile directory.
        """
        import shutil
        try:
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()