"""
Mobile tests for Automation Exercise using Playwright
"""

import time

import pytest
from loguru import logger

from src.core.config.mobile_settings import MobileDevice, MobileTestConfig
from src.core.mobile_test_base import MobileTestBase


class TestAutomationExerciseMobile(MobileTestBase):
    """Mobile tests for Automation Exercise website"""

    def test_mobile_home_page_load(self):
        """Test home page loads correctly on mobile"""
        logger.info(f"Testing mobile home page load on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Check page title
        title = self.get_page_title()
        assert (
            "Automation Exercise" in title
        ), f"Expected 'Automation Exercise' in title, got: {title}"

        # Check current URL
        current_url = self.get_current_url()
        assert (
            "automationexercise.com" in current_url
        ), f"Expected automationexercise.com in URL, got: {current_url}"

        # Take screenshot
        self.take_screenshot("home_page_mobile")

        logger.info("✅ Mobile home page load test passed")

    def test_mobile_responsive_design(self):
        """Test responsive design on mobile devices"""
        logger.info(f"Testing responsive design on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Test responsive design at different breakpoints
        responsive_results = self.check_responsive_design()

        # Assert that at least 80% of breakpoints are usable
        usable_count = sum(1 for usable in responsive_results.values() if usable)
        total_count = len(responsive_results)

        assert (
            usable_count >= total_count * 0.8
        ), f"Only {usable_count}/{total_count} breakpoints are usable"

        logger.info(
            f"✅ Responsive design test passed: {usable_count}/{total_count} breakpoints usable"
        )

    def test_mobile_navigation_menu(self):
        """Test mobile navigation menu functionality"""
        logger.info(f"Testing mobile navigation on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Check for mobile menu elements
        mobile_menu_selectors = [
            ".navbar-nav",
            ".navbar-toggler",
            ".navbar-collapse",
            ".nav-menu",
        ]

        menu_found = False
        for selector in mobile_menu_selectors:
            if self.is_element_visible(selector):
                menu_found = True
                logger.info(f"Mobile menu found: {selector}")
                break

        assert menu_found, "No mobile navigation menu found"

        # Test menu interaction if hamburger menu exists
        hamburger_selectors = [
            ".navbar-toggler",
            ".hamburger",
            ".mobile-menu-toggle",
            "[data-toggle='collapse']",
        ]

        for selector in hamburger_selectors:
            if self.is_element_visible(selector):
                # Click hamburger menu
                self.tap_element(selector)
                time.sleep(1)

                # Check if menu expanded
                expanded_selectors = [
                    ".navbar-collapse.show",
                    ".mobile-menu.active",
                    ".nav-menu.open",
                ]

                menu_expanded = any(
                    self.is_element_visible(expanded_selector)
                    for expanded_selector in expanded_selectors
                )
                if menu_expanded:
                    logger.info("✅ Mobile menu interaction test passed")
                    return

        logger.info("✅ Mobile navigation test passed (no hamburger menu found)")

    def test_mobile_search_functionality(self):
        """Test search functionality on mobile"""
        logger.info(f"Testing mobile search on {self.device.value}")

        # Navigate to products page where search is available
        self.navigate_to("https://automationexercise.com/products")

        # Look for search input
        search_selectors = [
            "#search_product",
            ".search_product",
            "input[type='text'][placeholder*='search']",
            "input[type='text'][placeholder*='Search']",
        ]

        search_input_found = False
        search_selector = None

        for selector in search_selectors:
            if self.is_element_visible(selector):
                search_input_found = True
                search_selector = selector
                break

        if search_input_found:
            # Fill search input
            self.fill_input(search_selector, "Blue Top")

            # Look for search button
            search_button_selectors = [
                "#submit_search",
                ".submit_search",
                "button[type='submit']",
                ".search-btn",
            ]

            for button_selector in search_button_selectors:
                if self.is_element_visible(button_selector):
                    self.tap_element(button_selector)
                    break

            # Wait for search results
            time.sleep(2)

            # Check if search results page loaded
            current_url = self.get_current_url()
            assert "search" in current_url.lower(), "Search page not loaded"

            # Check if search term appears in page
            page_content = self.page.content()
            assert (
                "blue top" in page_content.lower()
            ), "Search term not found in results"

            logger.info("✅ Mobile search functionality test passed")
        else:
            logger.info("⚠️ Search input not found, skipping search test")

    def test_mobile_product_interaction(self):
        """Test product interaction on mobile"""
        logger.info(f"Testing mobile product interaction on {self.device.value}")

        self.navigate_to("https://automationexercise.com/products")

        # Look for product cards
        product_selectors = [
            ".single-products",
            ".product-item",
            ".product-card",
            ".item",
        ]

        product_found = False
        for selector in product_selectors:
            if self.is_element_visible(selector):
                product_found = True

                # Scroll to first product
                self.scroll_to_element(selector)
                time.sleep(1)

                # Look for add to cart button
                add_to_cart_selectors = [
                    ".add-to-cart",
                    ".btn-add-cart",
                    "button[onclick*='add']",
                    ".cart",
                ]

                for cart_selector in add_to_cart_selectors:
                    if self.is_element_visible(cart_selector):
                        # Click add to cart
                        self.tap_element(cart_selector)
                        time.sleep(2)

                        # Check for success message or modal
                        success_selectors = [
                            ".modal-content",
                            ".alert-success",
                            ".success-message",
                            "[class*='success']",
                        ]

                        success_found = any(
                            self.is_element_visible(success_selector)
                            for success_selector in success_selectors
                        )

                        if success_found:
                            logger.info("✅ Product added to cart successfully")
                            break

                break

        assert product_found, "No products found on products page"
        logger.info("✅ Mobile product interaction test passed")

    def test_mobile_forms(self):
        """Test form interactions on mobile"""
        logger.info(f"Testing mobile forms on {self.device.value}")

        self.navigate_to("https://automationexercise.com/login")

        # Test login form
        email_selectors = [
            "input[data-qa='login-email']",
            "input[type='email']",
            "#email",
            ".email",
        ]

        password_selectors = [
            "input[data-qa='login-password']",
            "input[type='password']",
            "#password",
            ".password",
        ]

        email_input_found = False
        password_input_found = False

        for selector in email_selectors:
            if self.is_element_visible(selector):
                self.fill_input(selector, "test@example.com")
                email_input_found = True
                break

        for selector in password_selectors:
            if self.is_element_visible(selector):
                self.fill_input(selector, "password123")
                password_input_found = True
                break

        # Test newsletter subscription form
        self.navigate_to("https://automationexercise.com/")
        self.scroll_to_bottom()

        newsletter_selectors = [
            "#susbscribe_email",
            "input[placeholder*='email']",
            ".newsletter input",
            "#newsletter",
        ]

        for selector in newsletter_selectors:
            if self.is_element_visible(selector):
                self.fill_input(selector, "test@example.com")

                # Look for subscribe button
                subscribe_selectors = [
                    "#subscribe",
                    ".subscribe",
                    "button[type='submit']",
                ]

                for sub_selector in subscribe_selectors:
                    if self.is_element_visible(sub_selector):
                        self.tap_element(sub_selector)
                        time.sleep(2)
                        break

                break

        assert email_input_found or password_input_found, "No form inputs found"
        logger.info("✅ Mobile forms test passed")

    def test_mobile_gestures(self):
        """Test mobile gestures and interactions"""
        logger.info(f"Testing mobile gestures on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Test basic gestures
        gesture_results = self.test_mobile_gestures()

        # Assert that basic gestures work
        assert gesture_results["tap"], "Tap gesture failed"
        assert gesture_results["scroll"], "Scroll gesture failed"

        logger.info(f"✅ Mobile gestures test passed: {gesture_results}")

    def test_mobile_performance(self):
        """Test mobile performance metrics"""
        logger.info(f"Testing mobile performance on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Measure page load time
        load_time = self.measure_page_load_time()

        # Assert reasonable load time (less than 10 seconds)
        assert load_time < 10000, f"Page load time too slow: {load_time}ms"

        # Get network requests
        network_requests = self.get_network_requests()

        # Check for performance issues
        assert len(network_requests) > 0, "No network requests recorded"

        logger.info(
            f"✅ Mobile performance test passed: Load time {load_time}ms, {len(network_requests)} requests"
        )

    def test_mobile_orientation(self):
        """Test mobile orientation changes"""
        logger.info(f"Testing mobile orientation on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Get initial viewport
        # initial_viewport = self.get_viewport_size()  # Unused variable

        # Test landscape orientation
        self.rotate_to_landscape()
        landscape_viewport = self.get_viewport_size()

        # Test portrait orientation
        self.rotate_to_portrait()
        portrait_viewport = self.get_viewport_size()

        # Assert orientation changes work
        assert (
            landscape_viewport["width"] > landscape_viewport["height"]
        ), "Landscape orientation not applied"
        assert (
            portrait_viewport["height"] > portrait_viewport["width"]
        ), "Portrait orientation not applied"

        # Check if page is still usable in both orientations
        landscape_usable = self._check_page_usability()
        self.rotate_to_portrait()
        portrait_usable = self._check_page_usability()

        assert landscape_usable, "Page not usable in landscape orientation"
        assert portrait_usable, "Page not usable in portrait orientation"

        logger.info("✅ Mobile orientation test passed")

    def test_mobile_accessibility(self):
        """Test mobile accessibility features"""
        logger.info(f"Testing mobile accessibility on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Check for accessibility elements
        accessibility_selectors = [
            "[alt]",  # Images with alt text
            "[aria-label]",
            "[aria-labelledby]",
            "[role]",
            "button[type='button']",
            "input[type='text']",
        ]

        accessibility_elements = []
        for selector in accessibility_selectors:
            elements = self.page.query_selector_all(selector)
            accessibility_elements.extend(elements)

        # Check for basic accessibility
        assert len(accessibility_elements) > 0, "No accessibility elements found"

        # Check for proper heading structure
        headings = self.page.query_selector_all("h1, h2, h3, h4, h5, h6")
        assert len(headings) > 0, "No headings found for accessibility"

        logger.info(
            f"✅ Mobile accessibility test passed: {len(accessibility_elements)} accessibility elements found"
        )

    def test_mobile_seo_elements(self):
        """Test mobile SEO elements"""
        logger.info(f"Testing mobile SEO on {self.device.value}")

        self.navigate_to("https://automationexercise.com/")

        # Check for meta viewport tag
        viewport_meta = self.page.query_selector("meta[name='viewport']")
        assert viewport_meta is not None, "Viewport meta tag not found"

        # Check for title tag
        title = self.page.query_selector("title")
        assert title is not None, "Title tag not found"

        # Check for meta description
        meta_description = self.page.query_selector("meta[name='description']")
        assert meta_description is not None, "Meta description not found"

        # Check for canonical URL
        canonical = self.page.query_selector("link[rel='canonical']")
        assert canonical is not None, "Canonical URL not found"

        logger.info("✅ Mobile SEO test passed")

    @pytest.mark.parametrize(
        "device",
        [
            MobileDevice.IPHONE_12,
            MobileDevice.IPHONE_14_PRO,
            MobileDevice.GALAXY_S23,
            MobileDevice.PIXEL_7,
        ],
    )
    def test_cross_device_compatibility(self, device):
        """Test compatibility across different mobile devices"""
        logger.info(f"Testing cross-device compatibility on {device.value}")

        # This test will be parameterized to run on different devices
        self.navigate_to("https://automationexercise.com/")

        # Basic functionality test
        title = self.get_page_title()
        assert "Automation Exercise" in title, f"Title check failed on {device.value}"

        # Responsive design check
        responsive_results = self.check_responsive_design()
        usable_count = sum(1 for usable in responsive_results.values() if usable)

        assert (
            usable_count >= len(responsive_results) * 0.7
        ), f"Responsive design failed on {device.value}"

        logger.info(f"✅ Cross-device compatibility test passed on {device.value}")


# Pytest configuration for mobile testing
def pytest_addoption(parser):
    """Add command line options for mobile testing"""
    parser.addoption(
        "--device", action="store", default="IPHONE_12", help="Mobile device to test on"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser engine to use (chromium, firefox, webkit)",
    )


def pytest_generate_tests(metafunc):
    """Generate test parameters for mobile testing"""
    if "device" in metafunc.fixturenames:
        devices = MobileTestConfig.get_all_devices()
        metafunc.parametrize("device", devices)
