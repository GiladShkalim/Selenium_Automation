# HomePage.py

from selenium.webdriver.common.by import By
from Scraper.pages.base.BasePage import BasePage

class HomePage(BasePage):
    HOME_URL = "https://www.jemix.co.il/"

    def navigate_to_home(self):
        self.driver.get(self.HOME_URL)

    def click_login(self):
        login_button_locator = (By.LINK_TEXT, "Login")
        self.click(login_button_locator)

