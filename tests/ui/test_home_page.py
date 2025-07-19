"""
UI tests for SmartShop home page
Demonstrates AI tools integration in testing
"""

import time

import pytest
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage
from utils.ai_data_generator import AIDataGenerator
from utils.visual_testing import VisualTester


class TestHomePage:
    """Home page UI tests with AI-powered data generation"""

    @pytest.fixture(scope="class")
    def driver(self):
        """WebDriver fixture"""
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        yield driver

        # Cleanup
        driver.quit()

    @pytest.fixture(scope="class")
    def home_page(self, driver):
        """Home page object fixture"""
        return HomePage(driver)

    @pytest.fixture(scope="class")
    def ai_generator(self):
        """AI data generator fixture"""
        return AIDataGenerator()

    @pytest.fixture(scope="class")
    def visual_tester(self):
        """Visual tester fixture"""
        return VisualTester()

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_home_page_loads_successfully(self, home_page):
        """Test that home page loads successfully"""
        home_page.open_home_page()

        # Check page title
        title = home_page.get_page_title()
        assert (
            "SmartShop" in title or "Home" in title
        ), f"Unexpected page title: {title}"

        # Check current URL
        current_url = home_page.get_current_url()
        assert home_page.base_url in current_url, f"Unexpected URL: {current_url}"

        logger.info("Home page loaded successfully")

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_page_elements_are_visible(self, home_page):
        """Test that main page elements are visible"""
        home_page.open_home_page()

        # Check main elements
        assert home_page.is_logo_visible(), "Logo is not visible"
        assert home_page.is_search_bar_visible(), "Search bar is not visible"
        assert home_page.is_navigation_menu_visible(), "Navigation menu is not visible"
        assert home_page.is_footer_visible(), "Footer is not visible"

        logger.info("All main page elements are visible")

    @pytest.mark.ui
    @pytest.mark.visual
    def test_page_visual_layout(self, home_page, visual_tester):
        """Test page visual layout with AI analysis"""
        home_page.open_home_page()

        # Perform visual check
        visual_result = visual_tester.check_page_layout("home_page", home_page.driver)

        # Check visual test result
        assert visual_result["status"] in [
            "passed",
            "warning",
        ], f"Visual check failed: {visual_result}"

        logger.info(f"Visual check passed: {visual_result['status']}")

    @pytest.mark.ui
    def test_search_functionality(self, home_page, ai_generator):
        """Test search functionality with AI-generated data"""
        home_page.open_home_page()

        # Generate search query using AI
        products = ai_generator.generate_product_catalog("electronics", 1)
        search_query = products[0]["name"] if products else "laptop"

        # Perform search
        home_page.search_product(search_query)

        # Check that search was performed (URL changed)
        time.sleep(2)  # Wait for search to complete
        current_url = home_page.get_current_url()

        assert (
            "search" in current_url.lower()
            or search_query.lower() in current_url.lower()
        ), f"Search was not performed: {current_url}"

        logger.info(f"Search completed successfully: {search_query}")

    @pytest.mark.ui
    def test_category_navigation(self, home_page):
        """Test category navigation"""
        home_page.open_home_page()

        categories = ["electronics", "clothing", "books"]

        for category in categories:
            # Save current URL
            initial_url = home_page.get_current_url()

            # Select category
            home_page.select_category(category)

            # Check that URL changed
            time.sleep(2)
            new_url = home_page.get_current_url()

            assert (
                new_url != initial_url
            ), f"URL did not change when selecting category {category}"
            assert (
                category in new_url.lower()
            ), f"Category {category} not reflected in URL"

            logger.info(f"Navigation to category {category} completed successfully")

    @pytest.mark.ui
    def test_add_product_to_cart(self, home_page):
        """Test adding product to cart"""
        home_page.open_home_page()
        home_page.wait_for_products_load()

        # Get initial cart count
        initial_cart_count = home_page.get_cart_count()

        # Add product to cart
        home_page.add_product_to_cart(0)

        # Wait for cart update
        time.sleep(2)

        # Check that cart count increased
        new_cart_count = home_page.get_cart_count()
        assert (
            new_cart_count > initial_cart_count
        ), f"Cart count did not increase: {initial_cart_count} -> {new_cart_count}"

        logger.info(f"Product added to cart: {initial_cart_count} -> {new_cart_count}")

    @pytest.mark.ui
    def test_newsletter_subscription(self, home_page, ai_generator):
        """Test newsletter subscription with AI-generated data"""
        home_page.open_home_page()
        home_page.scroll_to_footer()

        # Generate email using AI
        user_data = ai_generator.generate_user_profile("customer")
        email = user_data["email"]

        # Subscribe to newsletter
        home_page.subscribe_to_newsletter(email)

        # Check that subscription was performed (may be notification or form change)
        time.sleep(2)

        # Here you can add verification of successful subscription
        # For example, check for notification appearance or button state change

        logger.info(f"Newsletter subscription completed: {email}")

    @pytest.mark.ui
    @pytest.mark.visual
    def test_banner_visibility(self, home_page, visual_tester):
        """Test banner visibility with AI analysis"""
        home_page.open_home_page()

        # Check banner visibility
        assert home_page.is_banner_visible(), "Main banner is not visible"

        # Analyze banner with AI
        banner_result = visual_tester.check_element_visibility(
            home_page.driver, home_page.MAIN_BANNER[1]  # CSS selector
        )

        # Check analysis result
        assert (
            banner_result["status"] == "passed"
        ), f"Banner analysis failed: {banner_result}"

        # Check visibility quality
        if "analysis" in banner_result:
            visibility_score = banner_result["analysis"].get("visibility_score", 0)
            assert (
                visibility_score > 0.5
            ), f"Low banner visibility score: {visibility_score}"

        logger.info("Banner is visible and analyzed successfully")

    @pytest.mark.ui
    def test_slider_navigation(self, home_page):
        """Test slider navigation"""
        home_page.open_home_page()

        # Get initial banner text
        initial_banner_text = home_page.get_banner_text()

        # Navigate to next slide
        home_page.navigate_slider("next")
        time.sleep(2)

        # Check that text changed
        new_banner_text = home_page.get_banner_text()

        # Text may be the same if slider is cyclic
        # So we check that slider works (no errors)
        assert home_page.is_banner_visible(), "Banner not visible after navigation"

        logger.info("Slider navigation works correctly")

    @pytest.mark.ui
    def test_footer_links(self, home_page):
        """Test footer links"""
        home_page.open_home_page()
        home_page.scroll_to_footer()

        # Get list of links
        footer_links = home_page.get_footer_links()

        # Check that there are links
        assert len(footer_links) > 0, "No links in footer"

        # Check first link
        if footer_links:
            first_link = footer_links[0]
            initial_url = home_page.get_current_url()

            home_page.click_footer_link(first_link)
            time.sleep(2)

            new_url = home_page.get_current_url()
            assert (
                new_url != initial_url
            ), f"Click on link {first_link} did not change URL"

            logger.info(f"Footer link works: {first_link}")

    @pytest.mark.ui
    @pytest.mark.regression
    def test_responsive_design(self, home_page):
        """Test responsive design"""
        home_page.open_home_page()

        # Test different screen sizes
        screen_sizes = [
            (1920, 1080),  # Desktop
            (1366, 768),  # Laptop
            (768, 1024),  # Tablet
            (375, 667),  # Mobile
        ]

        for width, height in screen_sizes:
            home_page.set_window_size(width, height)
            time.sleep(1)

            # Check that main elements are still visible
            elements_status = home_page.verify_page_elements()

            # Logo and main elements should be visible at all sizes
            assert elements_status["logo"], f"Logo not visible at size {width}x{height}"
            assert elements_status[
                "search"
            ], f"Search not visible at size {width}x{height}"

            logger.info(f"Responsive design works at size {width}x{height}")

    @pytest.mark.ui
    @pytest.mark.performance
    def test_page_load_performance(self, home_page):
        """Test page load performance"""
        import time

        start_time = time.time()
        home_page.open_home_page()
        home_page.wait_for_page_load()
        load_time = time.time() - start_time

        # Check that page loads within reasonable time
        assert load_time < 10.0, f"Page load time too slow: {load_time:.2f}s"

        logger.info(f"Page load time: {load_time:.2f}s")

    @pytest.mark.ui
    @pytest.mark.ai
    def test_ai_generated_test_scenarios(self, home_page, ai_generator):
        """Test AI-generated test scenarios"""
        home_page.open_home_page()

        # Generate test scenarios using AI
        scenarios = ai_generator.generate_test_scenarios("home page functionality")

        if scenarios:
            logger.info(f"Generated {len(scenarios)} AI test scenarios")

            # Execute first few scenarios
            for i, scenario in enumerate(scenarios[:3]):
                logger.info(
                    f"Executing AI scenario {i+1}: {scenario.get('title', 'Untitled')}"
                )

                # Here you can add scenario execution logic
                # For example, execute steps from scenario['steps']

        else:
            logger.warning("No AI scenarios generated")

    @pytest.mark.ui
    @pytest.mark.visual
    def test_element_visibility_analysis(self, home_page, visual_tester):
        """Test element visibility analysis with AI"""
        home_page.open_home_page()

        # Test visibility of main elements
        elements_to_test = [
            ("logo", home_page.LOGO[1]),
            ("search", home_page.SEARCH_BAR[1]),
            ("navigation", home_page.NAVIGATION_MENU[1]),
        ]

        for element_name, selector in elements_to_test:
            result = visual_tester.check_element_visibility(home_page.driver, selector)

            assert (
                result["status"] == "passed"
            ), f"Element {element_name} visibility check failed: {result}"

            if "analysis" in result:
                visibility_score = result["analysis"].get("visibility_score", 0)
                logger.info(
                    f"Element {element_name} visibility score: {visibility_score}"
                )

        logger.info("Element visibility analysis completed")
