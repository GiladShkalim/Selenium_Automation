"""
Test module for main navigation functionality.

This module contains test cases for verifying the proper navigation through
category items on the Jemix website. It follows the Page Object Model pattern
and implements best practices for Selenium automation testing.

Test Cases:
    - test_main_navigation: Verifies navigation through different category pages
"""

import unittest
import platform
import os
import tempfile
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Import page objects
from Scraper.pages.jemix.HomePage import HomePage
from Scraper.pages.jemix.CategoryPage import CategoryPage
from Scraper.config.settings import PAGES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestMainNavigation(unittest.TestCase):
    """Test suite for main navigation functionality on Jemix website"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test-wide resources."""
        logger.info("Setting up test suite resources")
        # Create a temporary directory for Chrome user data
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
        """Set up test case - runs before each test method"""
        logger.info("Setting up test environment")
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
            
            # Initialize page objects
            self.home_page = HomePage(self.driver)
            self.category_page = CategoryPage(self.driver, "")  # Base category page
            
            # Initialize ActionChains and WebDriverWait
            self.actions = ActionChains(self.driver)
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("WebDriver initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize test resources: {str(e)}")
            raise

    def test_main_navigation(self):
        """Test main navigation through category items"""
        try:
            logger.info("Starting main navigation test")
            
            # Navigate to homepage
            self.home_page.navigate_to_home()
            logger.info("Navigated to homepage")
            
            # Test navigation for each category
            for page in PAGES:
                if 'tag' in page['url']:  # Only test category pages
                    try:
                        logger.info(f"Testing navigation to {page['name']}")
                        
                        # Update category page URL
                        self.category_page = CategoryPage(self.driver, page['url'])
                        
                        # Navigate to category
                        self.category_page.navigate_to_category()
                        
                        # Verify URL
                        current_url = self.driver.current_url.rstrip('/')
                        expected_url = page['url'].rstrip('/')
                        
                        self.assertEqual(
                            current_url, 
                            expected_url,
                            f"URL mismatch for {page['name']}. Expected: {expected_url}, Got: {current_url}"
                        )
                        
                        logger.info(f"Successfully verified navigation to {page['name']}")
                        
                    except TimeoutException:
                        logger.error(f"Timeout while navigating to {page['name']}")
                        raise
                    except Exception as e:
                        logger.error(f"Error while testing {page['name']}: {str(e)}")
                        raise

        except WebDriverException as e:
            logger.error("WebDriver encountered an error")
            logger.error(f"WebDriver error details: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    def tearDown(self):
        """Clean up test-specific resources."""
        logger.info("Cleaning up test case resources")
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Failed to quit WebDriver: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test-wide resources."""
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