"""
Base class for mobile testing with Playwright
"""

import time
from typing import Any, Dict, Optional

import pytest
from loguru import logger
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.core.config.mobile_settings import MobileConfig, MobileDevice, MobileTestConfig


class MobileTestBase:
    """Base class for mobile testing with Playwright"""

    def __init__(self):
        # These will be set in setup_method
        self.device = None
        self.browser_type = None
        self.config = None
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def setup_method(self):
        """Setup method called before each test"""
        # Get device and browser from environment variables
        import os

        device_name = os.environ.get("MOBILE_DEVICE", "IPHONE_12")
        self.device = MobileDevice[device_name]
        self.browser_type = os.environ.get("MOBILE_BROWSER", "chromium")
        self.config = MobileTestConfig.get_config(self.device)

        self.playwright = sync_playwright().start()

        # Launch browser
        if self.browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(
                headless=self.config.headless, slow_mo=self.config.slow_mo
            )
        elif self.browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(
                headless=self.config.headless, slow_mo=self.config.slow_mo
            )
        elif self.browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(
                headless=self.config.headless, slow_mo=self.config.slow_mo
            )
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        # Create context with mobile configuration
        context_options = {
            "viewport": self.config.viewport,
            "user_agent": self.config.user_agent,
            "locale": self.config.locale,
            "timezone_id": self.config.timezone_id,
            "ignore_https_errors": self.config.ignore_https_errors,
            "java_script_enabled": self.config.java_script_enabled,
            "bypass_csp": self.config.bypass_csp,
            "color_scheme": self.config.color_scheme,
            "reduced_motion": self.config.reduced_motion,
            "forced_colors": self.config.forced_colors,
        }

        if self.config.geolocation:
            context_options["geolocation"] = self.config.geolocation

        if self.config.permissions:
            context_options["permissions"] = self.config.permissions

        if self.config.extra_http_headers:
            context_options["extra_http_headers"] = self.config.extra_http_headers

        self.context = self.browser.new_context(**context_options)
        self.page = self.context.new_page()

        # Set default timeout
        self.page.set_default_timeout(self.config.timeout)

        logger.info(
            f"Mobile test setup completed for {self.device.value} with {self.browser_type}"
        )

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

        logger.info(f"Mobile test teardown completed for {self.device.value}")

    def navigate_to(self, url: str):
        """Navigate to URL"""
        logger.info(f"Navigating to {url} on {self.device.value}")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name: str = None):
        """Take screenshot"""
        if not name:
            name = f"{self.device.value}_{int(time.time())}"

        screenshot_path = f"reports/screenshots/mobile_{name}.png"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def get_viewport_size(self) -> dict[str, int]:
        """Get current viewport size"""
        return self.page.viewport_size

    def set_viewport_size(self, width: int, height: int):
        """Set viewport size"""
        self.page.set_viewport_size({"width": width, "height": height})
        logger.info(f"Viewport size set to {width}x{height}")

    def rotate_to_landscape(self):
        """Rotate device to landscape orientation"""
        current_size = self.page.viewport_size
        if current_size["width"] < current_size["height"]:
            self.page.set_viewport_size(
                {"width": current_size["height"], "height": current_size["width"]}
            )
            logger.info("Rotated to landscape orientation")

    def rotate_to_portrait(self):
        """Rotate device to portrait orientation"""
        current_size = self.page.viewport_size
        if current_size["width"] > current_size["height"]:
            self.page.set_viewport_size(
                {"width": current_size["height"], "height": current_size["width"]}
            )
            logger.info("Rotated to portrait orientation")

    def tap_element(self, selector: str):
        """Tap element (mobile-friendly click)"""
        self.page.tap(selector)
        logger.info(f"Tapped element: {selector}")

    def swipe(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 500
    ):
        """Perform swipe gesture"""
        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(end_x, end_y, steps=10)
        self.page.mouse.up()
        logger.info(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")

    def pinch_zoom_in(self, x: int, y: int):
        """Pinch zoom in gesture"""
        # Simulate pinch zoom in with mouse wheel
        self.page.mouse.wheel(x, y, delta_y=-100)
        logger.info(f"Pinch zoom in at ({x}, {y})")

    def pinch_zoom_out(self, x: int, y: int):
        """Pinch zoom out gesture"""
        # Simulate pinch zoom out with mouse wheel
        self.page.mouse.wheel(x, y, delta_y=100)
        logger.info(f"Pinch zoom out at ({x}, {y})")

    def wait_for_element(self, selector: str, timeout: int = None):
        """Wait for element to be visible"""
        if timeout is None:
            timeout = self.config.timeout

        self.page.wait_for_selector(selector, timeout=timeout)
        logger.info(f"Element found: {selector}")

    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            element = self.page.query_selector(selector)
            return element.is_visible() if element else False
        except Exception:
            return False

    def get_element_text(self, selector: str) -> str:
        """Get element text"""
        element = self.page.query_selector(selector)
        return element.text_content() if element else ""

    def fill_input(self, selector: str, text: str):
        """Fill input field"""
        self.page.fill(selector, text)
        logger.info(f"Filled input {selector} with: {text}")

    def scroll_to_element(self, selector: str):
        """Scroll to element"""
        self.page.scroll_into_view_if_needed(selector)
        logger.info(f"Scrolled to element: {selector}")

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        logger.info("Scrolled to bottom of page")

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.page.evaluate("window.scrollTo(0, 0)")
        logger.info("Scrolled to top of page")

    def get_page_title(self) -> str:
        """Get page title"""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get current URL"""
        return self.page.url

    def wait_for_navigation(self):
        """Wait for navigation to complete"""
        self.page.wait_for_load_state("networkidle")

    def reload_page(self):
        """Reload current page"""
        self.page.reload()
        self.wait_for_navigation()
        logger.info("Page reloaded")

    def go_back(self):
        """Go back in browser history"""
        self.page.go_back()
        self.wait_for_navigation()
        logger.info("Navigated back")

    def go_forward(self):
        """Go forward in browser history"""
        self.page.go_forward()
        self.wait_for_navigation()
        logger.info("Navigated forward")

    def get_network_requests(self) -> list:
        """Get list of network requests"""
        return self.page.evaluate("() => performance.getEntriesByType('navigation')")

    def measure_page_load_time(self) -> float:
        """Measure page load time"""
        load_time = self.page.evaluate(
            """
            () => {
                const navigation = performance.getEntriesByType('navigation')[0];
                return navigation.loadEventEnd - navigation.loadEventStart;
            }
        """
        )
        logger.info(f"Page load time: {load_time}ms")
        return load_time

    def check_responsive_design(self, breakpoints: list = None) -> dict[str, bool]:
        """Check responsive design at different breakpoints"""
        if breakpoints is None:
            breakpoints = [
                {"width": 320, "height": 568},  # iPhone SE
                {"width": 375, "height": 667},  # iPhone 6/7/8
                {"width": 414, "height": 896},  # iPhone X/11/12
                {"width": 768, "height": 1024},  # iPad
                {"width": 1024, "height": 1366},  # iPad Pro
            ]

        results = {}
        current_url = self.page.url

        for breakpoint in breakpoints:
            self.set_viewport_size(breakpoint["width"], breakpoint["height"])
            time.sleep(1)  # Wait for layout to adjust

            # Check if page is usable at this breakpoint
            is_usable = self._check_page_usability()
            results[f"{breakpoint['width']}x{breakpoint['height']}"] = is_usable

            logger.info(
                f"Breakpoint {breakpoint['width']}x{breakpoint['height']}: {'✅' if is_usable else '❌'}"
            )

        return results

    def _check_page_usability(self) -> bool:
        """Check if page is usable at current viewport"""
        try:
            # Check if main navigation is accessible
            nav_selectors = [
                "nav",
                ".navbar",
                ".header",
                ".menu",
                ".hamburger",
                ".mobile-menu",
                ".navigation",
            ]

            nav_visible = any(
                self.is_element_visible(selector) for selector in nav_selectors
            )

            # Check if main content is visible
            content_selectors = [
                "main",
                ".content",
                ".container",
                ".wrapper",
                "article",
                ".main-content",
            ]

            content_visible = any(
                self.is_element_visible(selector) for selector in content_selectors
            )

            # Check if page is not broken (no horizontal scroll)
            has_horizontal_scroll = self.page.evaluate(
                """
                () => document.documentElement.scrollWidth > document.documentElement.clientWidth
            """
            )

            return nav_visible and content_visible and not has_horizontal_scroll

        except Exception as e:
            logger.error(f"Error checking page usability: {e}")
            return False

    def test_mobile_gestures(self):
        """Test basic mobile gestures"""
        results = {"tap": False, "swipe": False, "scroll": False, "pinch_zoom": False}

        try:
            # Test tap
            if self.page.query_selector("body"):
                self.page.tap("body")
                results["tap"] = True

            # Test swipe
            viewport = self.page.viewport_size
            self.swipe(
                viewport["width"] // 2,
                viewport["height"] // 2,
                viewport["width"] // 2,
                viewport["height"] // 4,
            )
            results["swipe"] = True

            # Test scroll
            self.scroll_to_bottom()
            self.scroll_to_top()
            results["scroll"] = True

            # Test pinch zoom
            viewport = self.page.viewport_size
            self.pinch_zoom_in(viewport["width"] // 2, viewport["height"] // 2)
            results["pinch_zoom"] = True

        except Exception as e:
            logger.error(f"Error testing mobile gestures: {e}")

        return results
