# CategoryPage.py

from selenium.webdriver.common.by import By
from Scraper.pages.base.BasePage import BasePage

class CategoryPage(BasePage):
    def __init__(self, driver, category_url):
        super().__init__(driver)
        self.category_url = category_url

    def navigate_to_category(self):
        self.driver.get(self.category_url)

    def get_item_list(self, item_class_name):
        # Retrieve a list of items (e.g., coupons, products) by class name
        item_locator = (By.CLASS_NAME, item_class_name)
        return self.driver.find_elements(*item_locator)

    def click_item(self, item_text):
        # Click a specific item by its text
        item_locator = (By.LINK_TEXT, item_text)
        self.click(item_locator)