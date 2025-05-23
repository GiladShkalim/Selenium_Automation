# CategoryPage.py
# define a base class for all category pages

# Example usage for the Fashion category 
#from Scraper.pages.jemix.CategoryPage import CategoryPage
#fashion_page = CategoryPage(driver, "https://www.jemix.co.il/tag/fashion/")
#fashion_page.navigate_to_category()
#coupons = fashion_page.get_item_list("coupon-class")  # Replace with actual class name
#fashion_page.click_item("Specific Coupon Text")

# Example usage for the Shopping category
#shopping_page = CategoryPage(driver, "https://www.jemix.co.il/tag/shopping/")
#shopping_page.navigate_to_category()
#products = shopping_page.get_item_list("product-class")  # Replace with actual class name
#shopping_page.click_item("Specific Product Name")

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