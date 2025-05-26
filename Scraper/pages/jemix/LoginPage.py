from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scraper.pages.base.BasePage import BasePage
import time

class LoginPage(BasePage):
    """Page object for the Login page with updated element locators for Ultimate Member form."""
    
    LOGIN_URL = "https://www.jemix.co.il/login/"
    
    # Updated element locators for Ultimate Member form
    LOGIN_ELEMENTS = {
        "username_field": (
            By.CSS_SELECTOR, 
            "input[name='log']#user-955ddae"
        ),
        "password_field": (
            By.CSS_SELECTOR, 
            "input[name='pwd']#password-955ddae"
        ),
        "login_button": (
            By.CSS_SELECTOR, 
            "button[type='submit'][name='wp-submit']"
        ),
        "login_form": (
            By.CSS_SELECTOR,
            "form.elementor-login"
        )
    }

    def navigate_to_login(self):
        """Navigate to the login page and wait for form to load."""
        self.driver.get(self.LOGIN_URL)
        # Wait for the login form to be present and visible
        form = self.wait_for_element(self.LOGIN_ELEMENTS["login_form"])
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(form)
        )

    def login(self, username, password):
        """
        Perform login with the given credentials.
        
        Args:
            username (str): User's email/username
            password (str): User's password
        """
        try:
            # Wait for and enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_ELEMENTS["username_field"])
            )
            username_field.clear()
            username_field.send_keys(username)
            
            # Small wait between fields
            time.sleep(1)
            
            # Wait for and enter password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_ELEMENTS["password_field"])
            )
            password_field.clear()
            password_field.send_keys(password)
            
            # Small wait before clicking
            time.sleep(1)
            
            # Wait for button to be clickable and click
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_ELEMENTS["login_button"])
            )
            
            # Try direct click first
            try:
                login_button.click()
            except:
                # If direct click fails, try JavaScript click
                self.driver.execute_script("arguments[0].click();", login_button)
            
            # Add a longer wait after form submission
            time.sleep(5)  # Increase from 3 to 5 seconds
            
            # Wait for URL change
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url != self.LOGIN_URL
            )
            
            # Additional wait for page load
            time.sleep(4)  # Increase from 2 to 4 seconds
            
        except Exception as e:
            # Log the page source for debugging
            print("Page source at time of error:")
            print(self.driver.page_source)
            raise e
