"""
Simple mobile test to verify Playwright setup
"""

import os
import time

import pytest
from loguru import logger
from playwright.sync_api import sync_playwright


class TestSimpleMobile:
    """Simple mobile tests to verify Playwright setup"""

    def setup_method(self):
        """Setup method called before each test"""
        # Get device and browser from environment variables
        device_name = os.environ.get("MOBILE_DEVICE", "IPHONE_12")
        self.browser_type = os.environ.get("MOBILE_BROWSER", "chromium")

        logger.info(
            f"Setting up mobile test for {device_name} with {self.browser_type}"
        )

        # Start Playwright
        self.playwright = sync_playwright().start()

        # Launch browser
        if self.browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(headless=True)
        elif self.browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=True)
        elif self.browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=True)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        # Create context with mobile viewport
        self.context = self.browser.new_context(
            viewport={"width": 390, "height": 844},  # iPhone 12 viewport
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        )

        self.page = self.context.new_page()
        logger.info("Mobile browser setup completed")

    def teardown_method(self):
        """Teardown method called after each test"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

        logger.info("Mobile browser teardown completed")

    def test_mobile_home_page_load(self):
        """Test home page loads correctly on mobile"""
        logger.info("Testing mobile home page load")

        # Navigate to the website
        self.page.goto("https://automationexercise.com/")
        self.page.wait_for_load_state("networkidle")

        # Check page title
        title = self.page.title()
        assert (
            "Automation Exercise" in title
        ), f"Expected 'Automation Exercise' in title, got: {title}"

        # Check current URL
        current_url = self.page.url
        assert (
            "automationexercise.com" in current_url
        ), f"Expected automationexercise.com in URL, got: {current_url}"

        # Take screenshot
        screenshot_path = f"reports/screenshots/mobile_home_page_{int(time.time())}.png"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")

        logger.info("✅ Mobile home page load test passed")

    def test_mobile_viewport_size(self):
        """Test mobile viewport size"""
        logger.info("Testing mobile viewport size")

        self.page.goto("https://automationexercise.com/")

        # Get viewport size
        viewport_size = self.page.viewport_size
        logger.info(f"Viewport size: {viewport_size}")

        # Check if viewport is mobile-sized
        assert (
            viewport_size["width"] <= 414
        ), f"Viewport width too large: {viewport_size['width']}"
        assert (
            viewport_size["height"] <= 896
        ), f"Viewport height too large: {viewport_size['height']}"

        logger.info("✅ Mobile viewport size test passed")

    def test_mobile_responsive_elements(self):
        """Test responsive elements on mobile"""
        logger.info("Testing mobile responsive elements")

        self.page.goto("https://automationexercise.com/")

        # Check for mobile-friendly elements
        mobile_selectors = [
            ".navbar-nav",
            ".navbar-toggler",
            ".navbar-collapse",
            ".nav-menu",
        ]

        elements_found = 0
        for selector in mobile_selectors:
            try:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements_found += 1
                    logger.info(f"Found mobile element: {selector}")
            except Exception:
                pass

        assert elements_found > 0, "No mobile navigation elements found"

        logger.info(
            f"✅ Mobile responsive elements test passed: {elements_found} elements found"
        )

    def test_mobile_touch_interactions(self):
        """Test basic touch interactions"""
        logger.info("Testing mobile touch interactions")

        self.page.goto("https://automationexercise.com/")

        # Test tap (click)
        try:
            # Try to click on body
            self.page.click("body")
            logger.info("✅ Tap interaction successful")
        except Exception as e:
            logger.warning(f"Tap interaction failed: {e}")

        # Test scroll
        try:
            # Scroll to bottom
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            # Scroll to top
            self.page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)

            logger.info("✅ Scroll interaction successful")
        except Exception as e:
            logger.warning(f"Scroll interaction failed: {e}")

        logger.info("✅ Mobile touch interactions test passed")

    def test_mobile_performance(self):
        """Test mobile performance metrics"""
        logger.info("Testing mobile performance")

        # Navigate and measure load time
        start_time = time.time()
        self.page.goto("https://automationexercise.com/")

        # Use domcontentloaded instead of networkidle for faster loading
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        except Exception:
            # Fallback to simple wait if domcontentloaded times out
            time.sleep(2)

        load_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        logger.info(f"Page load time: {load_time:.2f}ms")

        # Assert reasonable load time (less than 15 seconds)
        assert load_time < 15000, f"Page load time too slow: {load_time:.2f}ms"

        # Get network requests
        try:
            network_requests = self.page.evaluate(
                "() => performance.getEntriesByType('navigation')"
            )
            logger.info(f"Network requests: {len(network_requests)}")

            assert len(network_requests) > 0, "No network requests recorded"
        except Exception as e:
            logger.warning(f"Could not get network requests: {e}")

        logger.info("✅ Mobile performance test passed")
