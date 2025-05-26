from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Scraper.pages.base.BasePage import BasePage
from Scraper.config.settings import ACCOUNT_DASHBOARD_URL

class AccountPage(BasePage):
    """
    Page object for the Account/Dashboard page.
    Contains methods for verifying successful login via URL redirect.
    """
    
    def __init__(self, driver):
        """Initialize the AccountPage with a WebDriver instance."""
        super().__init__(driver)
        self.dashboard_url = ACCOUNT_DASHBOARD_URL

    def wait_for_dashboard_load(self, timeout=15):
        """
        Wait for the account dashboard page to load and verify URL.
        This is the only verification needed since only logged-in users can access this URL.
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if redirected to dashboard URL, False otherwise
        """
        try:
            # First wait for any intermediate redirects (like wp-login.php)
            WebDriverWait(self.driver, timeout).until(
                lambda driver: "wp-login.php" not in driver.current_url
            )
            
            # Then wait for and verify the final dashboard URL
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url == self.dashboard_url
            )
            return True
        except Exception:
            return False

    def get_current_url(self):
        """
        Get the current page URL.
        
        Returns:
            str: Current page URL
        """
        return self.driver.current_url
