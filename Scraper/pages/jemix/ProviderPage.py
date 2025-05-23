from selenium.webdriver.common.by import By
from Scraper.pages.base.BasePage import BasePage

class ProviderPage(BasePage):
    def __init__(self, driver, provider_url):
        super().__init__(driver)
        self.provider_url = provider_url

    def navigate_to_provider(self):
        self.driver.get(self.provider_url)

    def get_coupon_list(self, coupon_class_name):
        # Retrieve a list of coupon elements by class name
        coupon_locator = (By.CLASS_NAME, coupon_class_name)
        return self.driver.find_elements(*coupon_locator)

    def click_coupon(self, coupon_text):
        # Click a specific coupon by its text
        coupon_locator = (By.LINK_TEXT, coupon_text)
        self.click(coupon_locator)

    def get_coupon_details(self, detail_class_name):
        # Retrieve details of a coupon, such as description or discount
        detail_locator = (By.CLASS_NAME, detail_class_name)
        return [element.text for element in self.driver.find_elements(*detail_locator)]

    def apply_coupon(self, coupon_code):
        # Example method to apply a coupon code, assuming there's an input field
        coupon_input_locator = (By.ID, "coupon-code-input")  # Replace with actual ID
        self.enter_text(coupon_input_locator, coupon_code)
        apply_button_locator = (By.ID, "apply-coupon-button")  # Replace with actual ID
        self.click(apply_button_locator)
