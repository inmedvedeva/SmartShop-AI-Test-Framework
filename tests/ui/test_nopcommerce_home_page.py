"""
UI Tests for nopCommerce Home Page
Tests for https://demo.nopcommerce.com/
"""

import time

import pytest
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.nopcommerce_home_page import NopCommerceHomePage
from utils.ai_data_generator import AIDataGenerator


class TestNopCommerceHomePage:
    """Test class for nopCommerce Home Page"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test"""
        self.driver = driver
        self.home_page = NopCommerceHomePage(driver)
        self.ai_generator = AIDataGenerator()

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_home_page_loads_successfully(self):
        """Test that home page loads successfully"""
        logger.info("Testing home page loads successfully")

        # Open home page
        self.home_page.open_home_page()

        # Verify page title
        expected_title = "nopCommerce demo store"
        actual_title = self.home_page.get_page_title()
        assert (
            expected_title in actual_title
        ), f"Expected '{expected_title}' in title, got '{actual_title}'"

        # Verify page URL
        assert "demo.nopcommerce.com" in self.driver.current_url

        logger.info("✅ Home page loads successfully")

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_search_functionality(self):
        """Test search functionality"""
        logger.info("Testing search functionality")

        # Open home page
        self.home_page.open_home_page()

        # Search for a product
        search_term = "laptop"
        self.home_page.search_product(search_term)

        # Wait for search results
        time.sleep(2)

        # Verify search results page
        assert "search" in self.driver.current_url.lower()

        # Check if search term appears in results
        page_source = self.driver.page_source.lower()
        assert search_term in page_source or "no products" in page_source

        logger.info("✅ Search functionality works")

    @pytest.mark.ui
    def test_navigation_links(self):
        """Test navigation links"""
        logger.info("Testing navigation links")

        # Open home page
        self.home_page.open_home_page()

        # Test login link
        self.home_page.click_login()
        time.sleep(1)
        assert "login" in self.driver.current_url.lower()

        # Go back to home
        self.driver.back()
        time.sleep(1)

        # Test register link
        self.home_page.click_register()
        time.sleep(1)
        assert "register" in self.driver.current_url.lower()

        logger.info("✅ Navigation links work")

    @pytest.mark.ui
    def test_category_navigation(self):
        """Test category navigation"""
        logger.info("Testing category navigation")

        # Open home page
        self.home_page.open_home_page()

        # Test computers category
        self.home_page.click_category("computers")
        time.sleep(2)
        assert "computers" in self.driver.current_url.lower()

        # Go back to home
        self.driver.back()
        time.sleep(1)

        # Test electronics category
        self.home_page.click_category("electronics")
        time.sleep(2)
        assert "electronics" in self.driver.current_url.lower()

        logger.info("✅ Category navigation works")

    @pytest.mark.ui
    @pytest.mark.ai
    def test_featured_products_with_ai_data(self):
        """Test featured products using AI-generated data"""
        logger.info("Testing featured products with AI data")

        # Generate AI data
        user_data = self.ai_generator.generate_user_profile("customer")
        products_data = self.ai_generator.generate_product_catalog("electronics", 3)

        # Open home page
        self.home_page.open_home_page()

        # Get featured products from the page
        featured_products = self.home_page.get_featured_products()

        # Verify we have products
        assert len(featured_products) > 0, "No featured products found"

        # Log AI-generated data vs real products
        logger.info(
            f"AI-generated user: {user_data['first_name']} {user_data['last_name']}"
        )
        logger.info(f"AI-generated products: {[p['name'] for p in products_data]}")
        logger.info(
            f"Real featured products: {[p['title'] for p in featured_products[:3]]}"
        )

        # Verify product structure
        for product in featured_products[:3]:  # Check first 3 products
            assert "title" in product, "Product missing title"
            assert "price" in product, "Product missing price"
            assert "link" in product, "Product missing link"

        logger.info("✅ Featured products test with AI data completed")

    @pytest.mark.ui
    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        logger.info("Testing newsletter subscription")

        # Generate AI email
        user_data = self.ai_generator.generate_user_profile("customer")
        test_email = user_data["email"]

        # Open home page
        self.home_page.open_home_page()

        # Subscribe to newsletter
        self.home_page.subscribe_to_newsletter(test_email)
        time.sleep(2)

        # Check for success message (this might vary based on the site)
        page_source = self.driver.page_source.lower()
        success_indicators = ["thank you", "subscribed", "success", "newsletter"]
        has_success = any(indicator in page_source for indicator in success_indicators)

        # If no success message, at least verify the form was submitted
        if not has_success:
            # Check if email field is cleared (indicates form submission)
            email_field = self.driver.find_element(By.ID, "newsletter-email")
            assert (
                email_field.get_attribute("value") == ""
            ), "Email field should be cleared after submission"

        logger.info(
            f"✅ Newsletter subscription test completed with email: {test_email}"
        )

    @pytest.mark.ui
    def test_shopping_cart_access(self):
        """Test shopping cart access"""
        logger.info("Testing shopping cart access")

        # Open home page
        self.home_page.open_home_page()

        # Get initial cart count
        initial_count = self.home_page.get_cart_items_count()
        logger.info(f"Initial cart count: {initial_count}")

        # Click on shopping cart
        self.home_page.click_shopping_cart()
        time.sleep(2)

        # Verify we're on cart page
        assert "cart" in self.driver.current_url.lower()

        logger.info("✅ Shopping cart access works")

    @pytest.mark.ui
    @pytest.mark.visual
    def test_page_elements_visibility(self):
        """Test that key page elements are visible"""
        logger.info("Testing page elements visibility")

        # Open home page
        self.home_page.open_home_page()

        # Check key elements are visible
        elements_to_check = [
            self.home_page.SEARCH_BOX,
            self.home_page.LOGIN_LINK,
            self.home_page.REGISTER_LINK,
            self.home_page.SHOPPING_CART_LINK,
        ]

        for element_locator in elements_to_check:
            element = self.driver.find_element(*element_locator)
            assert element.is_displayed(), f"Element {element_locator} is not visible"

        # Check for featured products
        featured_products = self.driver.find_elements(*self.home_page.FEATURED_PRODUCTS)
        assert len(featured_products) > 0, "No featured products visible"

        logger.info("✅ All key page elements are visible")

    @pytest.mark.ui
    @pytest.mark.performance
    def test_page_load_performance(self):
        """Test page load performance"""
        logger.info("Testing page load performance")

        # Measure page load time
        start_time = time.time()
        self.home_page.open_home_page()
        load_time = time.time() - start_time

        # Verify page loads within reasonable time (10 seconds)
        assert load_time < 10, f"Page load took too long: {load_time:.2f} seconds"

        logger.info(f"✅ Page loaded in {load_time:.2f} seconds")

    @pytest.mark.ui
    def test_responsive_design(self):
        """Test responsive design (basic check)"""
        logger.info("Testing responsive design")

        # Open home page
        self.home_page.open_home_page()

        # Test different viewport sizes
        viewports = [
            (1920, 1080),  # Desktop
            (768, 1024),  # Tablet
            (375, 667),  # Mobile
        ]

        for width, height in viewports:
            self.driver.set_window_size(width, height)
            time.sleep(1)

            # Verify page still loads and key elements are present
            assert self.driver.title, "Page title should be present"

            # Check if search box is still accessible
            search_box = self.driver.find_element(*self.home_page.SEARCH_BOX)
            assert (
                search_box.is_displayed()
            ), f"Search box not visible at {width}x{height}"

        logger.info("✅ Responsive design test completed")
