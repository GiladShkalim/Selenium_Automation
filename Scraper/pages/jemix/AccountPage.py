from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Scraper.pages.base.BasePage import BasePage
from Scraper.config.settings import ACCOUNT_DASHBOARD_URL

class AccountPage(BasePage):
    """
    Page object for the Account/Dashboard page.
    Contains methods and locators for interacting with account-related elements.
    """
    
    # Element locators
    ACCOUNT_ELEMENTS = {
        "welcome_message": (By.CSS_SELECTOR, ".welcome-message"),
        "account_menu": (By.CSS_SELECTOR, ".account-navigation"),
        "logout_button": (By.CSS_SELECTOR, ".logout-button")
    }

    def __init__(self, driver):
        """Initialize the AccountPage with a WebDriver instance."""
        super().__init__(driver)
        self.dashboard_url = ACCOUNT_DASHBOARD_URL

    def is_user_logged_in(self):
        """
        Verify if user is logged in by checking for account-specific elements.
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        try:
            return all(
                self.wait_for_element(locator).is_displayed()
                for locator in self.ACCOUNT_ELEMENTS.values()
            )
        except Exception:
            return False

    def get_current_url(self):
        """
        Get the current page URL.
        
        Returns:
            str: Current page URL
        """
        return self.driver.current_url

    def wait_for_dashboard_load(self, timeout=10):
        """
        Wait for the account dashboard page to load completely.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if dashboard loaded successfully, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url == self.dashboard_url
            )
            return True
        except Exception:
            return False
