"""
Test module for Login functionality.

This module contains test cases for verifying the login functionality
of the Jemix website. It follows the Page Object Model pattern and implements
best practices for Selenium automation testing.

Test Cases:
    - test_valid_user_login: Verifies successful login with valid credentials
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from ....pages.jemix.LoginPage import LoginPage
from ....pages.jemix.AccountPage import AccountPage
from ....config.settings import TEST_USERS, ACCOUNT_DASHBOARD_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestLogin(unittest.TestCase):
    """Test suite for Login functionality."""

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
            
            # Initialize page objects
            self.login_page = LoginPage(self.driver)
            self.account_page = AccountPage(self.driver)
            logger.info("WebDriver and page objects initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize test resources: {str(e)}")
            raise

    def test_valid_user_login(self):
        """Test the login functionality with valid credentials.
        
        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Submit login form
        4. Verify redirect to account dashboard URL
        """
        try:
            logger.info("Starting valid user login test")
            
            # Arrange
            test_user = TEST_USERS["valid_user"]
            logger.info(f"Using test user: {test_user['username']}")
            
            # Act
            logger.info("Navigating to login page")
            self.login_page.navigate_to_login()
            
            # Log current URL before login attempt
            current_url = self.driver.current_url
            logger.info(f"Current URL before login: {current_url}")
            
            logger.info("Attempting login with valid credentials")
            try:
                self.login_page.login(
                    username=test_user["username"],
                    password=test_user["password"]
                )
            except Exception as e:
                logger.error(f"Login attempt failed: {str(e)}")
                raise
            
            # Assert
            try:
                # Wait for redirect and verify URL
                logger.info("Waiting for dashboard redirect")
                self.assertTrue(
                    self.account_page.wait_for_dashboard_load(),
                    "Failed to redirect to account dashboard"
                )
                
                # Verify final URL matches expected dashboard URL
                current_url = self.account_page.get_current_url()
                logger.info(f"Current URL after login: {current_url}")
                
                self.assertEqual(
                    current_url,
                    ACCOUNT_DASHBOARD_URL,
                    f"Expected URL {ACCOUNT_DASHBOARD_URL}, but got {current_url}"
                )
                
                logger.info("Login test completed successfully")
                
            except AssertionError as e:
                logger.error(f"Login verification failed: {str(e)}")
                raise
            
        except TimeoutException as e:
            logger.error("Page load or element interaction timed out")
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