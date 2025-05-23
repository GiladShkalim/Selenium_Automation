"""
Test module for HomePage functionality
"""

import unittest
import platform
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ....pages.jemix.HomePage import HomePage
from ....config.settings import BASE_URL

class TestHomePageLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test-wide resources"""
        # Create a temporary directory for Chrome user data
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")

    def setUp(self):
        """Set up test-specific resources"""
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

        try:
            # Initialize Chrome driver with automatic ChromeDriver management
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        except Exception as e:
            print(f"Failed to initialize Chrome driver: {str(e)}")
            raise

        self.home_page = HomePage(self.driver)

    def test_homepage_loads_successfully(self):
        """Test the homepage loading functionality"""
        try:
            # Navigate to the homepage
            self.home_page.navigate_to_home()
            
            # Wait for and verify the page title
            self.assertIn("jemix", self.driver.title.lower(), "Page title should contain 'jemix'")
            
            # Basic checks for common elements that should be present
            self.assertTrue(
                self.home_page.wait_for_element(("tag name", "header")), 
                "Header section not found"
            )
            self.assertTrue(
                self.home_page.wait_for_element(("tag name", "nav")), 
                "Navigation section not found"
            )
            self.assertTrue(
                self.home_page.wait_for_element(("tag name", "footer")), 
                "Footer section not found"
            )
        except Exception as e:
            print(f"Test failed with error: {str(e)}")
            raise

    def tearDown(self):
        """Clean up test-specific resources"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Failed to quit driver: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test-wide resources"""
        import shutil
        try:
            # Remove the temporary Chrome profile directory
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Failed to clean up temporary directory: {str(e)}")

if __name__ == "__main__":
    unittest.main()