"""
Test module for Category Navigation functionality.

This module contains test cases for verifying the navigation between different
categories and the proper loading of provider lists for each category.
"""

import unittest
import platform
import os
import tempfile
import logging
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestCategoryNavigation(unittest.TestCase):
    """Test suite for category navigation functionality."""
    
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup - runs once before all tests.
        Creates a temporary directory for Chrome user data.
        """
        logger.info("Setting up test suite resources")
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
        """
        Method-level setup - runs before each test method.
        Initializes WebDriver and page objects.
        """
        logger.info("Setting up test case resources")
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
            
            # Enable logging
            chrome_options.add_argument("--enable-logging")
            chrome_options.add_argument("--v=1")

            # Use headless mode in WSL or CI environments
            if platform.system() == "Linux" and "microsoft" in platform.uname().release.lower():
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--headless=new")

            # Initialize Chrome driver with automatic ChromeDriver management
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Set implicit wait time
            self.driver.implicitly_wait(10)
            
            # Initialize category pages
            self.category_pages = {}
            for page in PAGES:
                if page["name"] not in ["Home", "login", "account"]:
                    self.category_pages[page["name"]] = CategoryPage(self.driver, page["url"])
            
            logger.info("WebDriver and page objects initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize test resources: {str(e)}")
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
            provider_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "elementor-posts-container"))
            )
            
            # Verify providers are present
            providers = provider_list.find_elements(By.CLASS_NAME, "elementor-post")
            
            # Verify at least one provider is present
            if len(providers) == 0:
                logger.warning(f"No providers found for category: {category_name}")
                return False
                
            # Verify each provider has required elements
            for provider in providers:
                try:
                    # Check for thumbnail link
                    provider.find_element(By.CLASS_NAME, "elementor-post__thumbnail__link")
                    # Check for thumbnail image
                    provider.find_element(By.CLASS_NAME, "elementor-post__thumbnail")
                except NoSuchElementException:
                    logger.warning(f"Provider missing required elements in category: {category_name}")
                    return False
                    
            logger.info(f"Successfully verified {len(providers)} providers for category: {category_name}")
            return True
            
        except TimeoutException:
            logger.error(f"Timeout waiting for provider list in category: {category_name}")
            return False
        except Exception as e:
            logger.error(f"Error verifying provider list: {str(e)}")
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
                logger.info(f"Navigating to category: {category_name}")
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
                
                logger.info(f"Successfully verified category: {category_name}")
                
            except AssertionError as ae:
                logger.error(f"Assertion failed for category {category_name}: {str(ae)}")
                raise
            except Exception as e:
                logger.error(f"Error testing category {category_name}: {str(e)}")
                raise

    def tearDown(self):
        """
        Method-level cleanup - runs after each test method.
        Closes the WebDriver instance.
        """
        logger.info("Cleaning up test case resources")
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Failed to quit WebDriver: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """
        Class-level cleanup - runs once after all tests.
        Removes the temporary Chrome profile directory.
        """
        logger.info("Cleaning up test suite resources")
        import shutil
        try:
            # Remove the temporary Chrome profile directory
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
            logger.info("Temporary directory cleaned up successfully")
        except Exception as e:
            logger.error(f"Failed to clean up temporary directory: {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)