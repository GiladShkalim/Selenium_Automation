"""
Test module for HomePage functionality.

This module contains test cases for verifying the proper loading and element presence
of the Jemix homepage. It follows the Page Object Model pattern and implements
best practices for Selenium automation testing.

Test Cases:
    - test_homepage_loads_successfully: Verifies that the homepage loads and all key elements are present
"""

import unittest
import platform
import os
import tempfile
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from ....pages.jemix.HomePage import HomePage
from ....config.settings import BASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestHomePageLoad(unittest.TestCase):
    """Test suite for HomePage loading functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test-wide resources."""
        logger.info("Setting up test suite resources")
        # Create a temporary directory for Chrome user data
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
        """Set up test-specific resources."""
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

            # Use headless mode in WSL or CI environments
            if platform.system() == "Linux" and "microsoft" in platform.uname().release.lower():
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--headless=new")

            # Initialize Chrome driver with automatic ChromeDriver management
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.home_page = HomePage(self.driver)
            logger.info("WebDriver initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize test resources: {str(e)}")
            raise

    def test_homepage_loads_successfully(self):
        """Test the homepage loading functionality.
        
        Steps:
        1. Navigate to homepage
        2. Verify page title
        3. Check presence of all key elements
        """
        try:
            logger.info("Starting homepage load test")
            
            # Arrange & Act
            self.home_page.navigate_to_home()
            logger.info("Navigated to homepage")
            
            # Assert page title
            try:
                self.assertIn("jemix", self.driver.title.lower(), 
                            "Page title should contain 'jemix'")
                logger.info("Page title verified")
            except AssertionError as e:
                logger.error(f"Page title verification failed: {str(e)}")
                logger.info(f"Actual page title: {self.driver.title}")
                raise
            
            # Assert all elements are present
            element_status = self.home_page.verify_all_elements()
            failed_elements = []
            
            for element_key, is_visible in element_status.items():
                try:
                    self.assertTrue(
                        is_visible,
                        f"Element '{element_key}' should be visible on the homepage"
                    )
                    logger.info(f"Element '{element_key}' verified successfully")
                except AssertionError:
                    failed_elements.append(element_key)
                    logger.warning(f"Element '{element_key}' verification failed")
            
            if failed_elements:
                raise AssertionError(
                    f"The following elements were not found or not visible: {', '.join(failed_elements)}"
                )
            
            logger.info("All homepage elements verified successfully")

        except TimeoutException as e:
            logger.error("Page load timed out")
            logger.error(f"Timeout details: {str(e)}")
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

if __name__ == "__main__":
    unittest.main()