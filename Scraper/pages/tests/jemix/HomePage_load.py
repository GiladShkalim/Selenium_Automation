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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from ....pages.jemix.HomePage import HomePage
from ....config.settings import BASE_URL

class TestHomePageLoad(unittest.TestCase):
    """Test suite for HomePage loading functionality."""

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

        except Exception as e:
            raise

    def test_homepage_loads_successfully(self):
        """Test the homepage loading functionality."""
        try:
            self.home_page.navigate_to_home()
            
            # Assert page title
            self.assertIn("jemix", self.driver.title.lower(), 
                        "Page title should contain 'jemix'")
            
            # Assert all elements are present
            element_status = self.home_page.verify_all_elements()
            failed_elements = []
            
            for element_key, is_visible in element_status.items():
                if not is_visible:
                    failed_elements.append(element_key)
            
            if failed_elements:
                raise AssertionError(
                    f"The following elements were not found or not visible: {', '.join(failed_elements)}"
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