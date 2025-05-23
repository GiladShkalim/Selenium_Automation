# create test files - jemix test - name files by test types.

import unittest
from selenium import webdriver
from Scraper.pages.jemix.HomePage import HomePage
from Scraper.config.settings import BASE_URL

class TestHomePageLoad(unittest.TestCase):
    # @before
    def setUp(self):
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()  # Ensure the correct driver is installed and in PATH
        self.home_page = HomePage(self.driver)

    # @test
    def test_homepage_loads_successfully(self):
        # Navigate to the homepage
        self.home_page.navigate_to_home()

        # Assertions to verify key elements are present and visible
        self.assertTrue(self.home_page.wait_for_element(("id", "logo-id")), "Logo is not visible")  # Replace with actual ID
        self.assertTrue(self.home_page.wait_for_element(("id", "nav-id")), "Navigation is not visible")  # Replace with actual ID
        self.assertTrue(self.home_page.wait_for_element(("id", "banner-id")), "Banner is not visible")  # Replace with actual ID

    # @after
    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()


