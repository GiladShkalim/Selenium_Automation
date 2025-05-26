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
    # Element locators
    PROVIDER_ARTICLE = (By.CSS_SELECTOR, "article.elementor-post")
    PROVIDER_LINK = (By.CSS_SELECTOR, "a.elementor-post__thumbnail__link")
    PROVIDER_THUMBNAIL = (By.CSS_SELECTOR, "div.elementor-post__thumbnail img")

    def __init__(self, driver, category_url):
        super().__init__(driver)
        self.category_url = category_url

    def navigate_to_category(self):
        """Navigate to the category page"""
        self.driver.get(self.category_url)

    def get_item_list(self, item_class_name):
        # Retrieve a list of items (e.g., coupons, products) by class name
        item_locator = (By.CLASS_NAME, item_class_name)
        return self.driver.find_elements(*item_locator)

    def click_item(self, item_text):
        # Click a specific item by its text
        item_locator = (By.LINK_TEXT, item_text)
        self.click(item_locator)

    def get_provider_articles(self):
        """Get all provider articles in the category page
        
        Returns:
            list: List of article elements
        """
        return self.driver.find_elements(*self.PROVIDER_ARTICLE)

    def get_provider_links(self):
        """Get all provider links in the category page
        
        Returns:
            list: List of provider URLs
        """
        links = []
        articles = self.get_provider_articles()
        for article in articles:
            try:
                link = article.find_element(*self.PROVIDER_LINK)
                links.append({
                    'url': link.get_attribute('href'),
                    'title': link.get_attribute('href').split('/')[-2].replace('-coupon', '').replace('-', ' ').title()
                })
            except:
                # Article without link is valid, continue to next
                continue
        return links

    def verify_provider_thumbnails(self):
        """Verify that provider articles with links have thumbnails
        
        Returns:
            bool: True if all linked articles have thumbnails
        """
        articles = self.get_provider_articles()
        for article in articles:
            try:
                link = article.find_element(*self.PROVIDER_LINK)
                # If there's a link, there should be a thumbnail
                thumbnail = article.find_element(*self.PROVIDER_THUMBNAIL)
                if not thumbnail.get_attribute('src'):
                    return False
            except:
                # Articles without links can skip thumbnail check
                continue
        return True

    def has_provider_content(self):
        """Check if the category page has any provider content
        
        Returns:
            bool: True if at least one provider article exists
        """
        return len(self.get_provider_articles()) > 0