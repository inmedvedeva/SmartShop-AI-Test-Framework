"""
UI Tests for Automation Exercise Home Page
Tests for https://automationexercise.com/
"""

import time

import pytest
from loguru import logger

from pages.automation_exercise_home_page import AutomationExerciseHomePage
from utils.ai_data_generator import AIDataGenerator


class TestAutomationExerciseHomePage:
    """Test class for Automation Exercise Home Page"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test environment"""
        self.driver = driver
        self.home_page = AutomationExerciseHomePage(driver)
        self.ai_generator = AIDataGenerator()

    def test_home_page_load(self):
        """Test home page loads successfully"""
        logger.info("Testing home page load")

        self.home_page.open_home_page()
        title = self.home_page.get_page_title()

        assert (
            "Automation Exercise" in title
        ), f"Expected 'Automation Exercise' in title, got: {title}"
        assert (
            self.driver.current_url == "https://automationexercise.com/"
        ), f"Expected URL: https://automationexercise.com/, got: {self.driver.current_url}"

        logger.info(f"✅ Home page loaded successfully: {title}")

    def test_search_functionality(self):
        """Test search functionality"""
        logger.info("Testing search functionality")

        self.home_page.open_home_page()

        # Test search for a product
        search_term = "dress"
        self.home_page.search_product(search_term)
        time.sleep(2)

        # Verify search results page
        assert "search" in self.driver.current_url.lower(), "Search page not loaded"
        logger.info(f"✅ Search functionality works for: {search_term}")

    def test_navigation_links(self):
        """Test navigation menu links"""
        logger.info("Testing navigation links")

        self.home_page.open_home_page()

        # Test Products link
        self.home_page.click_products()
        time.sleep(2)
        assert "products" in self.driver.current_url.lower(), "Products page not loaded"
        logger.info("✅ Products link works")

        # Go back to home
        self.driver.back()
        time.sleep(1)

        # Test Cart link
        self.home_page.click_cart()
        time.sleep(2)
        assert "cart" in self.driver.current_url.lower(), "Cart page not loaded"
        logger.info("✅ Cart link works")

        # Go back to home
        self.driver.back()
        time.sleep(1)

        # Test Signup/Login link
        self.home_page.click_signup_login()
        time.sleep(2)
        assert "login" in self.driver.current_url.lower(), "Login page not loaded"
        logger.info("✅ Signup/Login link works")

    def test_test_cases_page(self):
        """Test Test Cases page"""
        logger.info("Testing Test Cases page")

        self.home_page.open_home_page()
        self.home_page.click_test_cases()
        time.sleep(2)

        assert (
            "test_cases" in self.driver.current_url.lower()
        ), "Test Cases page not loaded"
        logger.info("✅ Test Cases page works")

    def test_api_testing_page(self):
        """Test API Testing page"""
        logger.info("Testing API Testing page")

        self.home_page.open_home_page()
        self.home_page.click_api_testing()
        time.sleep(2)

        assert (
            "api_list" in self.driver.current_url.lower()
        ), "API Testing page not loaded"
        logger.info("✅ API Testing page works")

    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        logger.info("Testing newsletter subscription")

        self.home_page.open_home_page()

        # Generate AI email
        user_data = self.ai_generator.generate_user_profile("customer")
        test_email = user_data["email"]

        # Subscribe to newsletter
        self.home_page.subscribe_to_newsletter(test_email)
        time.sleep(2)

        # Check subscription success
        success = self.home_page.is_newsletter_subscribed()
        assert success, "Newsletter subscription failed"

        logger.info(f"✅ Newsletter subscription successful with: {test_email}")

    def test_featured_products(self):
        """Test featured products display"""
        logger.info("Testing featured products")

        self.home_page.open_home_page()

        # Get featured products
        products = self.home_page.get_featured_products()

        assert len(products) > 0, "No featured products found"

        # Log product details
        for i, product in enumerate(products[:3]):  # Show first 3 products
            logger.info(f"   Product {i+1}: {product['name']} - {product['price']}")

        logger.info(f"✅ Found {len(products)} featured products")

    def test_ai_integration(self):
        """Test AI data integration with UI testing"""
        logger.info("Testing AI data integration")

        self.home_page.open_home_page()

        # Generate AI data
        user_data = self.ai_generator.generate_user_profile("customer")
        products_data = self.ai_generator.generate_product_catalog("clothing", 3)

        # Get real products from page
        real_products = self.home_page.get_featured_products()

        logger.info(f"🤖 AI User: {user_data['first_name']} {user_data['last_name']}")
        logger.info(f"🤖 AI Products: {[p['name'] for p in products_data]}")
        logger.info(f"🛍️ Real Products: {[p['name'] for p in real_products[:3]]}")

        assert len(real_products) > 0, "No real products found on page"
        assert len(products_data) > 0, "No AI products generated"

        logger.info("✅ AI integration test completed")

    def test_responsive_design(self):
        """Test responsive design on different screen sizes"""
        logger.info("Testing responsive design")

        viewports = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile"),
        ]

        for width, height, device in viewports:
            self.driver.set_window_size(width, height)
            time.sleep(1)

            self.home_page.open_home_page()
            time.sleep(2)

            # Check if page loads without errors
            title = self.home_page.get_page_title()
            assert "Automation Exercise" in title, f"Page not loaded on {device}"

            logger.info(f"✅ {device} viewport ({width}x{height}) works")

    def test_page_performance(self):
        """Test page load performance"""
        logger.info("Testing page performance")

        start_time = time.time()
        self.home_page.open_home_page()
        load_time = time.time() - start_time

        logger.info(f"⏱️ Page load time: {load_time:.2f} seconds")

        # Performance assertions
        assert load_time < 10, f"Page load too slow: {load_time:.2f}s"

        if load_time < 3:
            logger.info("✅ Excellent performance")
        elif load_time < 5:
            logger.info("✅ Good performance")
        else:
            logger.info("⚠️ Moderate performance")

    def test_page_elements_visibility(self):
        """Test key page elements are visible"""
        logger.info("Testing page elements visibility")

        self.home_page.open_home_page()

        # Check key elements
        elements_to_check = [
            ("Header", self.home_page.HEADER),
            ("Logo", self.home_page.LOGO),
            ("Search Box", self.home_page.SEARCH_BOX),
            ("Products Link", self.home_page.PRODUCTS_LINK),
            ("Cart Link", self.home_page.CART_LINK),
            ("Signup/Login Link", self.home_page.SIGNUP_LOGIN_LINK),
        ]

        for element_name, locator in elements_to_check:
            try:
                element = self.driver.find_element(*locator)
                assert element.is_displayed(), f"{element_name} is not visible"
                logger.info(f"✅ {element_name}: Visible")
            except Exception as e:
                logger.error(f"❌ {element_name}: Error - {e}")
                raise

    @pytest.mark.smoke
    def test_smoke_test(self):
        """Smoke test - basic functionality"""
        logger.info("Running smoke test")

        # Test basic page load
        self.home_page.open_home_page()
        title = self.home_page.get_page_title()
        assert "Automation Exercise" in title

        # Test basic navigation
        self.home_page.click_products()
        time.sleep(1)
        assert "products" in self.driver.current_url.lower()

        logger.info("✅ Smoke test passed")

    @pytest.mark.ai
    def test_ai_powered_testing(self):
        """AI-powered test scenario"""
        logger.info("Running AI-powered test")

        # Generate dynamic test data
        user_data = self.ai_generator.generate_user_profile("customer")
        search_terms = self.ai_generator.generate_search_terms(3)

        self.home_page.open_home_page()

        # Test search with AI-generated terms
        for term in search_terms:
            self.home_page.search_product(term)
            time.sleep(1)
            assert "search" in self.driver.current_url.lower()
            self.driver.back()
            time.sleep(1)

        logger.info(
            f"✅ AI-powered test completed with {len(search_terms)} search terms"
        )
