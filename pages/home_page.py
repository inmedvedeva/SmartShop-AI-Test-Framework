"""
SmartShop Home Page
"""

from loguru import logger
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    """Class for working with home page"""

    # Element locators
    LOGO = (By.CSS_SELECTOR, ".logo")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon")
    CART_COUNT = (By.CSS_SELECTOR, ".cart-count")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-btn")
    REGISTER_BUTTON = (By.CSS_SELECTOR, ".register-btn")
    USER_MENU = (By.CSS_SELECTOR, ".user-menu")

    # Product categories
    CATEGORY_MENU = (By.CSS_SELECTOR, ".category-menu")
    ELECTRONICS_CATEGORY = (By.CSS_SELECTOR, "a[href*='electronics']")
    CLOTHING_CATEGORY = (By.CSS_SELECTOR, "a[href*='clothing']")
    BOOKS_CATEGORY = (By.CSS_SELECTOR, "a[href*='books']")

    # Banners and sliders
    MAIN_BANNER = (By.CSS_SELECTOR, ".main-banner")
    BANNER_SLIDER = (By.CSS_SELECTOR, ".banner-slider")
    SLIDER_NEXT = (By.CSS_SELECTOR, ".slider-next")
    SLIDER_PREV = (By.CSS_SELECTOR, ".slider-prev")

    # Featured products
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".featured-products")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-title")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".add-to-cart-btn")

    # Footer
    FOOTER = (By.CSS_SELECTOR, "footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a")
    NEWSLETTER_INPUT = (By.CSS_SELECTOR, ".newsletter-input")
    NEWSLETTER_SUBMIT = (By.CSS_SELECTOR, ".newsletter-submit")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/"

    def open_home_page(self):
        """Opens home page"""
        self.open(self.url)
        self.wait_for_page_load()
        logger.info("Home page opened")

    def search_product(self, query: str):
        """
        Searches for product

        Args:
            query: Search query
        """
        self.input_text(self.SEARCH_INPUT, query)
        self.click_element(self.SEARCH_BUTTON)
        logger.info(f"Product search: {query}")

    def get_cart_count(self) -> int:
        """Gets number of items in cart"""
        try:
            count_text = self.get_text(self.CART_COUNT)
            return int(count_text) if count_text.isdigit() else 0
        except:
            return 0

    def click_cart(self):
        """Clicks on cart"""
        self.click_element(self.CART_ICON)
        logger.info("Navigated to cart")

    def click_login(self):
        """Clicks on login button"""
        self.click_element(self.LOGIN_BUTTON)
        logger.info("Navigated to login page")

    def click_register(self):
        """Clicks on register button"""
        self.click_element(self.REGISTER_BUTTON)
        logger.info("Navigated to register page")

    def select_category(self, category: str):
        """
        Selects product category

        Args:
            category: Category name
        """
        category_locators = {
            "electronics": self.ELECTRONICS_CATEGORY,
            "clothing": self.CLOTHING_CATEGORY,
            "books": self.BOOKS_CATEGORY,
        }

        if category in category_locators:
            self.click_element(category_locators[category])
            logger.info(f"Category selected: {category}")
        else:
            logger.error(f"Category not found: {category}")

    def get_featured_products(self) -> list:
        """Gets list of featured products"""
        products = []
        product_cards = self.find_elements(self.PRODUCT_CARDS)

        for card in product_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, ".product-title").text
                price = card.find_element(By.CSS_SELECTOR, ".product-price").text
                products.append({"title": title, "price": price})
            except:
                continue

        logger.info(f"Found featured products: {len(products)}")
        return products

    def add_product_to_cart(self, product_index: int = 0):
        """
        Adds product to cart

        Args:
            product_index: Product index (first by default)
        """
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)

        if product_index < len(add_buttons):
            add_buttons[product_index].click()
            logger.info(f"Product {product_index} added to cart")
        else:
            logger.error(f"Product with index {product_index} not found")

    def subscribe_to_newsletter(self, email: str):
        """
        Subscribes to newsletter

        Args:
            email: Email for subscription
        """
        self.input_text(self.NEWSLETTER_INPUT, email)
        self.click_element(self.NEWSLETTER_SUBMIT)
        logger.info(f"Newsletter subscription: {email}")

    def is_user_logged_in(self) -> bool:
        """Checks if user is logged in"""
        return self.is_element_visible(self.USER_MENU)

    def get_user_menu_text(self) -> str:
        """Gets user menu text"""
        if self.is_user_logged_in():
            return self.get_text(self.USER_MENU)
        return ""

    def navigate_slider(self, direction: str = "next"):
        """
        Navigates slider

        Args:
            direction: Direction (next/prev)
        """
        if direction == "next":
            self.click_element(self.SLIDER_NEXT)
        elif direction == "prev":
            self.click_element(self.SLIDER_PREV)

        logger.info(f"Slider navigation: {direction}")

    def get_banner_text(self) -> str:
        """Gets main banner text"""
        return self.get_text(self.MAIN_BANNER)

    def is_banner_visible(self) -> bool:
        """Checks banner visibility"""
        return self.is_element_visible(self.MAIN_BANNER)

    def get_footer_links(self) -> list:
        """Gets list of footer links"""
        links = self.find_elements(self.FOOTER_LINKS)
        return [link.text for link in links if link.text]

    def click_footer_link(self, link_text: str):
        """
        Clicks on footer link

        Args:
            link_text: Link text
        """
        links = self.find_elements(self.FOOTER_LINKS)

        for link in links:
            if link.text == link_text:
                link.click()
                logger.info(f"Footer link clicked: {link_text}")
                return

        logger.error(f"Link not found: {link_text}")

    def verify_page_elements(self) -> dict:
        """Checks presence of main page elements"""
        elements_status = {
            "logo": self.is_element_visible(self.LOGO),
            "search": self.is_element_visible(self.SEARCH_INPUT),
            "cart": self.is_element_visible(self.CART_ICON),
            "login": self.is_element_visible(self.LOGIN_BUTTON),
            "register": self.is_element_visible(self.REGISTER_BUTTON),
            "banner": self.is_element_visible(self.MAIN_BANNER),
            "featured_products": self.is_element_visible(self.FEATURED_PRODUCTS),
            "footer": self.is_element_visible(self.FOOTER),
        }

        logger.info(f"Page elements status: {elements_status}")
        return elements_status

    def get_page_title(self) -> str:
        """Gets page title"""
        return self.get_title()

    def wait_for_products_load(self, timeout: int = 10):
        """
        Waits for products to load

        Args:
            timeout: Wait timeout
        """
        self.wait_for_element_visible(self.FEATURED_PRODUCTS, timeout)
        logger.info("Products loaded")

    def scroll_to_products(self):
        """Scrolls to products section"""
        self.scroll_to_element(self.FEATURED_PRODUCTS)
        logger.info("Scrolled to products")

    def scroll_to_footer(self):
        """Scrolls to footer"""
        self.scroll_to_element(self.FOOTER)
        logger.info("Scrolled to footer")
