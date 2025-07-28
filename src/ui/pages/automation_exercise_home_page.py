"""
Automation Exercise Home Page Object Model
Page Object for https://automationexercise.com/
"""

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.ui.pages.base_home_page import BaseHomePage


class AutomationExerciseHomePage(BaseHomePage):
    """Page Object for Automation Exercise Home Page"""

    # Header elements
    HEADER = (By.CSS_SELECTOR, ".header-middle")
    LOGO = (By.CSS_SELECTOR, ".logo a")
    SEARCH_BOX = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")

    # Navigation menu
    HOME_LINK = (By.CSS_SELECTOR, "a[href='/']")
    PRODUCTS_LINK = (By.CSS_SELECTOR, "a[href='/products']")
    CART_LINK = (By.CSS_SELECTOR, "a[href='/view_cart']")
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    TEST_CASES_LINK = (By.CSS_SELECTOR, "a[href='/test_cases']")
    API_TESTING_LINK = (By.CSS_SELECTOR, "a[href='/api_list']")
    VIDEO_TUTORIALS_LINK = (By.CSS_SELECTOR, "a[href='/video_tutorials']")
    CONTACT_US_LINK = (By.CSS_SELECTOR, "a[href='/contact_us']")

    # User account elements
    LOGGED_IN_USER = (By.CSS_SELECTOR, ".fa-user")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")

    # Main content
    SLIDER = (By.CSS_SELECTOR, ".carousel-inner")
    FEATURES = (By.CSS_SELECTOR, ".features_items")

    # Product elements
    PRODUCTS = (By.CSS_SELECTOR, ".single-products")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".productinfo h2")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".add-to-cart")
    VIEW_PRODUCT_BUTTONS = (By.CSS_SELECTOR, ".choose a")

    # Newsletter
    NEWSLETTER_EMAIL = (By.ID, "susbscribe_email")
    NEWSLETTER_SUBSCRIBE_BUTTON = (By.ID, "subscribe")

    # Footer
    FOOTER = (By.CSS_SELECTOR, ".footer-widget")
    SUBSCRIPTION_SUCCESS = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver):
        super().__init__(driver, "https://automationexercise.com/")

    def get_expected_title(self) -> str:
        """Get expected page title"""
        return "Automation Exercise"

    def get_expected_url(self) -> str:
        """Get expected page URL"""
        return "automationexercise.com"

    def search_product(self, product_name: str):
        """Search for a product"""
        logger.info(f"Searching for product: {product_name}")
        search_box = self.find_element(self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(product_name)
        self.click_element(self.SEARCH_BUTTON)
        return self

    def click_products(self):
        """Click on Products link"""
        logger.info("Clicking on Products link")
        self.click_element(self.PRODUCTS_LINK)
        return self

    def click_cart(self):
        """Click on Cart link"""
        logger.info("Clicking on Cart link")
        self.click_element(self.CART_LINK)
        return self

    def click_signup_login(self):
        """Click on Signup/Login link"""
        logger.info("Clicking on Signup/Login link")
        self.click_element(self.SIGNUP_LOGIN_LINK)
        return self

    def click_test_cases(self):
        """Click on Test Cases link"""
        logger.info("Clicking on Test Cases link")
        self.click_element(self.TEST_CASES_LINK)
        return self

    def click_api_testing(self):
        """Click on API Testing link"""
        logger.info("Clicking on API Testing link")
        self.click_element(self.API_TESTING_LINK)
        return self

    def click_video_tutorials(self):
        """Click on Video Tutorials link"""
        logger.info("Clicking on Video Tutorials link")
        self.click_element(self.VIDEO_TUTORIALS_LINK)
        return self

    def click_contact_us(self):
        """Click on Contact Us link"""
        logger.info("Clicking on Contact Us link")
        self.click_element(self.CONTACT_US_LINK)
        return self

    def get_featured_products(self):
        """Get list of featured products"""
        logger.info("Getting featured products")
        products = self.find_elements(self.PRODUCTS)
        product_list = []

        for product in products:
            try:
                name_element = product.find_element(By.CSS_SELECTOR, ".productinfo p")
                price_element = product.find_element(By.CSS_SELECTOR, ".productinfo h2")

                product_list.append(
                    {"name": name_element.text, "price": price_element.text}
                )
            except Exception:
                logger.warning("Could not get product info")

        return product_list

    def subscribe_to_newsletter(self, email: str):
        """Subscribe to newsletter"""
        logger.info(f"Subscribing to newsletter with email: {email}")
        email_field = self.find_element(self.NEWSLETTER_EMAIL)
        email_field.clear()
        email_field.send_keys(email)
        self.click_element(self.NEWSLETTER_SUBSCRIBE_BUTTON)
        # Wait for the success message to appear
        import time

        time.sleep(2)
        return self

    def is_newsletter_subscribed(self, timeout=5):
        """Check if newsletter subscription was successful (wait for message to appear)"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            success_message = wait.until(
                EC.visibility_of_element_located(self.SUBSCRIPTION_SUCCESS)
            )
            logger.info(f"Newsletter subscription message: '{success_message.text}'")
            return (
                "you have been successfully subscribed!"
                in success_message.text.strip().lower()
            )
        except Exception:
            logger.warning("Could not get newsletter subscription message")
            return False

    # get_page_title is inherited from BaseHomePage

    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            logged_in_element = self.find_element(self.LOGGED_IN_USER)
            return logged_in_element.is_displayed()
        except Exception:
            return False

    def logout(self):
        """Logout user"""
        logger.info("Logging out user")
        self.click_element(self.LOGOUT_LINK)
        return self

    def delete_account(self):
        """Delete user account"""
        logger.info("Deleting user account")
        self.click_element(self.DELETE_ACCOUNT_LINK)
        return self

    def get_cart_items_count(self):
        """Get number of items in cart"""
        try:
            cart_link = self.find_element(self.CART_LINK)
            cart_text = cart_link.text
            # Extract number from cart text if present
            import re

            match = re.search(r"\((\d+)\)", cart_text)
            return int(match.group(1)) if match else 0
        except Exception:
            return 0

    def add_product_to_cart(self, product_index: int = 0):
        """Add a product to cart by index"""
        logger.info(f"Adding product {product_index} to cart")
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if add_buttons and len(add_buttons) > product_index:
            add_buttons[product_index].click()
            return True
        return False

    def view_product(self, product_index: int = 0):
        """View product details by index"""
        logger.info(f"Viewing product {product_index}")
        view_buttons = self.find_elements(self.VIEW_PRODUCT_BUTTONS)
        if view_buttons and len(view_buttons) > product_index:
            view_buttons[product_index].click()
            return True
        return False
