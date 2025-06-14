"""
Test module for main navigation functionality.

This module contains test cases for verifying the proper navigation through
category items on the Jemix website. It follows the Page Object Model pattern
and implements best practices for Selenium automation testing.

Test Cases:
    - test_main_navigation: Verifies navigation through different category pages
    - Verifies provider articles presence and validity in each category
"""

import unittest
import platform
import os
import tempfile
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
from Scraper.pages.jemix.ProviderPage import ProviderPage
from Scraper.config.settings import PAGES

class TestMainNavigation(unittest.TestCase):
    """Test suite for main navigation functionality on Jemix website"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test-wide resources."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.user_data_dir = os.path.join(cls.temp_dir, "chrome_test_profile")
        cls.category_results = {}

    def setUp(self):
        """Set up test case - runs before each test method"""
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

        except Exception as e:
            raise

    def verify_category_providers(self, category_name, category_url):
        """Verify providers in a category page
        
        Args:
            category_name (str): Name of the category
            category_url (str): URL of the category page
            
        Returns:
            dict: Results of provider verification
        """
        results = {
            'category': category_name,
            'url': category_url,
            'has_content': False,
            'provider_count': 0,
            'providers': [],
            'thumbnails_valid': False
        }
        
        try:
            # Check if category has any provider content
            has_content = self.category_page.has_provider_content()
            results['has_content'] = has_content
            
            if has_content:
                # Get all provider links
                provider_links = self.category_page.get_provider_links()
                results['provider_count'] = len(provider_links)
                results['providers'] = provider_links
                
                # Verify thumbnails
                results['thumbnails_valid'] = self.category_page.verify_provider_thumbnails()
            
            return results
            
        except Exception as e:
            results['error'] = str(e)
            return results

    def test_main_navigation(self):
        """Test main navigation through category items"""
        try:
            # Navigate to homepage
            self.home_page.navigate_to_home()
            
            # Test navigation for each category
            for page in PAGES:
                if 'tag' in page['url']:  # Only test category pages
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
                        f"URL mismatch for {page['name']}"
                    )
                    
                    # Verify providers in the category
                    provider_results = self.verify_category_providers(page['name'], page['url'])
                    self.category_results[page['name']] = provider_results
                    
                    # Basic assertions for provider content
                    self.assertTrue(
                        provider_results['has_content'],
                        f"No provider content found in {page['name']}"
                    )
                    
                    if provider_results['provider_count'] > 0:
                        self.assertTrue(
                            provider_results['thumbnails_valid'],
                            f"Invalid thumbnails found in {page['name']}"
                        )

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
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()