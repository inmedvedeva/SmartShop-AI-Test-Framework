"""
nopCommerce Home Page Object Model
Page Object for https://demo.nopcommerce.com/
"""

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class NopCommerceHomePage(BasePage):
    """Page Object for nopCommerce Home Page"""

    # Locators
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search-box-button")
    LOGIN_LINK = (By.CSS_SELECTOR, "a.ico-login")
    REGISTER_LINK = (By.CSS_SELECTOR, "a.ico-register")
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, "a.ico-cart")
    WISHLIST_LINK = (By.CSS_SELECTOR, "a.ico-wishlist")
    ACCOUNT_LINK = (By.CSS_SELECTOR, "a.ico-account")

    # Product categories
    COMPUTERS_LINK = (By.CSS_SELECTOR, "a[href*='/computers']")
    ELECTRONICS_LINK = (By.CSS_SELECTOR, "a[href*='/electronics']")
    APPAREL_LINK = (By.CSS_SELECTOR, "a[href*='/apparel']")
    DIGITAL_DOWNLOADS_LINK = (By.CSS_SELECTOR, "a[href*='/digital-downloads']")
    BOOKS_LINK = (By.CSS_SELECTOR, "a[href*='/books']")
    JEWELRY_LINK = (By.CSS_SELECTOR, "a[href*='/jewelry']")
    GIFT_CARDS_LINK = (By.CSS_SELECTOR, "a[href*='/gift-cards']")

    # Featured products
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-title a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".actual-price")

    # Newsletter
    NEWSLETTER_EMAIL = (By.ID, "newsletter-email")
    NEWSLETTER_SUBSCRIBE_BUTTON = (By.ID, "newsletter-subscribe-button")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://demo.nopcommerce.com/"

    def open_home_page(self):
        """Open the home page"""
        logger.info(f"Opening nopCommerce home page: {self.url}")
        self.driver.get(self.url)

        # Wait for Cloudflare protection to pass
        logger.info("Waiting for Cloudflare protection to pass...")
        try:
            # Wait for "Just a moment..." to disappear
            WebDriverWait(self.driver, 30).until_not(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Just a moment')]")
                )
            )
            logger.info("Cloudflare protection passed")
        except Exception as e:
            logger.warning(f"Cloudflare wait timeout: {e}")

        # Additional wait for page to fully load
        self.wait_for_page_load()
        return self

    def search_product(self, product_name: str):
        """Search for a product"""
        logger.info(f"Searching for product: {product_name}")
        search_box = self.find_element(self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(product_name)
        self.click_element(self.SEARCH_BUTTON)
        return self

    def click_login(self):
        """Click on login link"""
        logger.info("Clicking on login link")
        self.click_element(self.LOGIN_LINK)
        return self

    def click_register(self):
        """Click on register link"""
        logger.info("Clicking on register link")
        self.click_element(self.REGISTER_LINK)
        return self

    def click_shopping_cart(self):
        """Click on shopping cart link"""
        logger.info("Clicking on shopping cart link")
        self.click_element(self.SHOPPING_CART_LINK)
        return self

    def click_category(self, category_name: str):
        """Click on a product category"""
        logger.info(f"Clicking on category: {category_name}")
        category_map = {
            "computers": self.COMPUTERS_LINK,
            "electronics": self.ELECTRONICS_LINK,
            "apparel": self.APPAREL_LINK,
            "digital-downloads": self.DIGITAL_DOWNLOADS_LINK,
            "books": self.BOOKS_LINK,
            "jewelry": self.JEWELRY_LINK,
            "gift-cards": self.GIFT_CARDS_LINK,
        }

        if category_name.lower() in category_map:
            self.click_element(category_map[category_name.lower()])
        else:
            logger.warning(f"Category '{category_name}' not found")

        return self

    def get_featured_products(self):
        """Get list of featured products"""
        logger.info("Getting featured products")
        products = self.find_elements(self.FEATURED_PRODUCTS)
        product_list = []

        for product in products:
            try:
                title_element = product.find_element(
                    By.CSS_SELECTOR, ".product-title a"
                )
                price_element = product.find_element(By.CSS_SELECTOR, ".actual-price")

                product_list.append(
                    {
                        "title": title_element.text,
                        "price": price_element.text,
                        "link": title_element.get_attribute("href"),
                    }
                )
            except Exception as e:
                logger.warning(f"Could not extract product info: {e}")

        return product_list

    def subscribe_to_newsletter(self, email: str):
        """Subscribe to newsletter"""
        logger.info(f"Subscribing to newsletter with email: {email}")
        email_field = self.find_element(self.NEWSLETTER_EMAIL)
        email_field.clear()
        email_field.send_keys(email)
        self.click_element(self.NEWSLETTER_SUBSCRIBE_BUTTON)
        return self

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            account_link = self.find_element(self.ACCOUNT_LINK)
            return "account" in account_link.get_attribute("href")
        except:
            return False

    def get_cart_items_count(self):
        """Get number of items in cart"""
        try:
            cart_link = self.find_element(self.SHOPPING_CART_LINK)
            cart_text = cart_link.text
            # Extract number from cart text (e.g., "Shopping cart (2)")
            import re

            match = re.search(r"\((\d+)\)", cart_text)
            return int(match.group(1)) if match else 0
        except:
            return 0
