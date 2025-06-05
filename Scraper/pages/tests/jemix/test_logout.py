import unittest
import platform
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from ....config.settings import TEST_USERS, ACCOUNT_DASHBOARD_URL
from ...jemix.HomePage import HomePage
from ...jemix.LoginPage import LoginPage
from ...jemix.AccountPage import AccountPage
from .LoginPage_test import TestLogin

class TestLogout(TestLogin):
    """Test case for user logout functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up test-wide resources."""
        # Create a temporary directory for Chrome user data
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
        """Set up test-specific resources."""
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
            
            # Set implicit wait time
            self.driver.implicitly_wait(10)
            
            # Initialize page objects
            self.login_page = LoginPage(self.driver)
            self.account_page = AccountPage(self.driver)

        except Exception as e:
            raise

    def test_user_logout(self):
        """Test the user logout process."""
        try:
            # Login first
            test_user = TEST_USERS["valid_user"]
            self.login_page.navigate_to_login()
            self.login_page.login(
                username=test_user["username"],
                password=test_user["password"]
            )
            
            # Verify login before proceeding
            if not self.account_page.wait_for_dashboard_load():
                self.skipTest("Login prerequisite failed - skipping logout test")
            
            # Perform and verify logout
            logout_success = self.account_page.logout()
            self.assertTrue(logout_success, "Logout operation failed")

        except Exception as e:
            raise

    def tearDown(self):
        """Clean up test-specific resources."""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception:
                pass

    @classmethod
    def tearDownClass(cls):
        """Clean up test-wide resources."""
        import shutil
        try:
            # Remove the temporary Chrome profile directory
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main() 