from selenium.webdriver.common.by import By
from Scraper.pages.base.BasePage import BasePage

class LoginPage(BasePage):
    LOGIN_URL = "https://www.jemix.co.il/login/"

    def navigate_to_login(self):
        self.driver.get(self.LOGIN_URL)

    def login(self, username, password):
        username_locator = (By.ID, "username")
        password_locator = (By.ID, "password")
        login_button_locator = (By.ID, "loginButton")

        self.enter_text(username_locator, username)
        self.enter_text(password_locator, password)
        self.click(login_button_locator)
