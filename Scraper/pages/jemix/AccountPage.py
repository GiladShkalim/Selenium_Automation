from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Scraper.pages.base.BasePage import BasePage
from Scraper.config.settings import ACCOUNT_DASHBOARD_URL
from selenium.common.exceptions import TimeoutException
import logging

class AccountPage(BasePage):
    """
    Page object for the Account/Dashboard page.
    Contains methods for verifying successful login via URL redirect.
    """
    
    # Locators
    LOGOUT_LINK = (By.XPATH, "//span[contains(@class, 'elementor-button-text') and text()='התנתקות']")
    CONFIRM_LOGOUT_LINK = (By.XPATH, "//div[@class='wp-die-message']//a[contains(@href, 'action=logout')]")
    
    def __init__(self, driver):
        """Initialize the AccountPage with a WebDriver instance."""
        super().__init__(driver)
        self.dashboard_url = ACCOUNT_DASHBOARD_URL
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(self.driver, 10)

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

    def logout(self):
        """
        Performs the logout operation and verifies successful logout
        Returns:
            bool: True if logout was successful, False otherwise
        """
        try:
            # Click the initial logout link
            self.wait_and_click(*self.LOGOUT_LINK)

            # Wait for and click the confirmation logout link if present
            try:
                self.wait_and_click(*self.CONFIRM_LOGOUT_LINK)
            except TimeoutException:
                # If no confirmation needed, proceed
                pass

            # Wait for redirect to login page (replacing wait_for_url_contains)
            self.wait.until(
                lambda driver: "/login/" in driver.current_url
            )
            
            return True
        except TimeoutException as e:
            return False

    def wait_and_click(self, by, value):
        """Wait for element to be clickable and click it."""
        element = self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
