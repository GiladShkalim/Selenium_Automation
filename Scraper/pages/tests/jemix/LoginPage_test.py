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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from ....pages.jemix.LoginPage import LoginPage
from ....pages.jemix.AccountPage import AccountPage
from ....config.settings import TEST_USERS, ACCOUNT_DASHBOARD_URL

class TestLogin(unittest.TestCase):
    """Test suite for Login functionality."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
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

        except Exception as e:
            raise

    def test_valid_user_login(self):
        """Test the login functionality with valid credentials."""
        try:
            test_user = TEST_USERS["valid_user"]
            self.login_page.navigate_to_login()
            
            self.login_page.login(
                username=test_user["username"],
                password=test_user["password"]
            )
            
            # Assert successful login
            self.assertTrue(
                self.account_page.wait_for_dashboard_load(),
                "Failed to redirect to account dashboard"
            )
            
            current_url = self.account_page.get_current_url()
            self.assertEqual(
                current_url,
                ACCOUNT_DASHBOARD_URL,
                f"Expected URL {ACCOUNT_DASHBOARD_URL}, but got {current_url}"
            )

        except Exception as e:
            raise

    def tearDown(self):
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception:
                pass

    @classmethod
    def tearDownClass(cls):
        import shutil
        try:
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        except Exception:
            pass

if __name__ == "__main__":
    unittest.main()