# HomePage.py

from selenium.webdriver.common.by import By
from Scraper.pages.base.BasePage import BasePage

class HomePage(BasePage):
    # Page URL
    HOME_URL = "https://www.jemix.co.il/"

    # Element locators using Elementor-specific classes from the site
    HOME_ELEMENTS = {
        "header": (By.CSS_SELECTOR, ".elementor-location-header"),
        "nav": (By.CSS_SELECTOR, ".elementor-element-110e30f nav, .elementor-nav-menu--main"),
        "main_content": (By.CSS_SELECTOR, ".elementor-section-wrap, .elementor-element-populated"),
        "footer": (By.CSS_SELECTOR, ".elementor-location-footer")
    }

    # Category links visible in the screenshot
    CATEGORY_LINKS = {
        "electronics": (By.CSS_SELECTOR, "a[href*='electronics']"),
        "food": (By.CSS_SELECTOR, "a[href*='food']"),
        "fashion": (By.CSS_SELECTOR, "a[href*='fashion']"),
        "shopping": (By.CSS_SELECTOR, "a[href*='shopping']")
    }

    def navigate_to_home(self):
        """Navigate to the homepage"""
        self.driver.get(self.HOME_URL)

    def verify_element_presence(self, element_key):
        """Verify if a specific element is present and visible
        
        Args:
            element_key (str): Key from HOME_ELEMENTS dictionary
            
        Returns:
            bool: True if element is present and visible
        """
        locator = self.HOME_ELEMENTS.get(element_key)
        if not locator:
            raise ValueError(f"Element key '{element_key}' not found in HOME_ELEMENTS")
        try:
            element = self.wait_for_element(locator)
            return element.is_displayed()
        except Exception as e:
            print(f"Failed to verify element '{element_key}': {str(e)}")
            return False

    def verify_all_elements(self):
        """Verify all home page elements are present and visible
        
        Returns:
            dict: Dictionary with element keys and their visibility status
        """
        return {key: self.verify_element_presence(key) for key in self.HOME_ELEMENTS}

    def click_login(self):
        """Click the login button"""
        login_button_locator = (By.LINK_TEXT, "Login")
        self.click(login_button_locator)

