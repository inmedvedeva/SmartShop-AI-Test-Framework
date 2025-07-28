"""
Base test classes with common functionality
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from loguru import logger


class BaseHomePageTest(ABC):
    """Base class for home page tests with common functionality"""

    @abstractmethod
    def get_home_page(self):
        """Get home page object - to be implemented by subclasses"""
        pass

    @abstractmethod
    def get_expected_title(self) -> str:
        """Get expected page title - to be implemented by subclasses"""
        pass

    @abstractmethod
    def get_expected_url(self) -> str:
        """Get expected page URL - to be implemented by subclasses"""
        pass

    def test_home_page_load(self):
        """Common test for home page load"""
        logger.info("Testing home page load")

        home_page = self.get_home_page()
        home_page.open_home_page()

        # Verify page load
        assert home_page.verify_home_page_load(), "Home page did not load correctly"

        # Additional verification
        title = home_page.get_page_title()
        url = home_page.get_current_url()

        expected_title = self.get_expected_title()
        expected_url = self.get_expected_url()

        assert (
            expected_title in title
        ), f"Expected '{expected_title}' in title, got: {title}"
        assert expected_url in url, f"Expected '{expected_url}' in URL, got: {url}"

        logger.info(f"✅ Home page loaded successfully: {title}")

    def test_page_performance(self):
        """Common test for page performance"""
        logger.info("Testing page performance")

        home_page = self.get_home_page()

        # Measure page load time
        start_time = time.time()
        home_page.open_home_page()
        load_time = time.time() - start_time

        # Assert reasonable load time (less than 15 seconds)
        assert load_time < 15, f"Page load time too slow: {load_time:.2f}s"

        logger.info(f"✅ Page performance test passed: {load_time:.2f}s")


class BaseSearchTest(ABC):
    """Base class for search functionality tests"""

    @abstractmethod
    def get_search_page(self):
        """Get page object with search functionality - to be implemented by subclasses"""
        pass

    @abstractmethod
    def navigate_to_search_page(self):
        """Navigate to page with search functionality - to be implemented by subclasses"""
        pass

    def test_search_functionality(self, search_term: str = "Blue Top"):
        """Common test for search functionality"""
        logger.info(f"Testing search functionality with term: {search_term}")

        search_page = self.get_search_page()
        self.navigate_to_search_page()

        # Perform search
        search_page.search_product(search_term)
        time.sleep(2)

        # Verify search results
        current_url = search_page.get_current_url()
        assert "search" in current_url.lower(), "Search page not loaded"

        # Check if search term appears in page content
        page_source = search_page.driver.page_source.lower()
        assert (
            search_term.lower() in page_source
        ), f"Search term '{search_term}' not found in results"

        logger.info(f"✅ Search functionality works for: {search_term}")


class BaseMobileTest(ABC):
    """Base class for mobile tests with common functionality"""

    @abstractmethod
    def get_mobile_page(self):
        """Get mobile page object - to be implemented by subclasses"""
        pass

    def test_mobile_home_page_load(self):
        """Common test for mobile home page load"""
        logger.info("Testing mobile home page load")

        mobile_page = self.get_mobile_page()
        mobile_page.navigate_to("https://automationexercise.com/")

        # Check page title
        title = mobile_page.get_page_title()
        assert (
            "Automation Exercise" in title
        ), f"Expected 'Automation Exercise' in title, got: {title}"

        # Check current URL
        current_url = mobile_page.get_current_url()
        assert (
            "automationexercise.com" in current_url
        ), f"Expected automationexercise.com in URL, got: {current_url}"

        # Take screenshot
        mobile_page.take_screenshot("home_page_mobile")

        logger.info("✅ Mobile home page load test passed")

    def test_mobile_performance(self):
        """Common test for mobile performance"""
        logger.info("Testing mobile performance")

        mobile_page = self.get_mobile_page()

        # Navigate and measure load time
        start_time = time.time()
        mobile_page.navigate_to("https://automationexercise.com/")

        # Wait for page to load with shorter timeout
        try:
            mobile_page.page.wait_for_load_state("domcontentloaded", timeout=10000)
        except Exception:
            # If domcontentloaded fails, just wait a bit
            time.sleep(2)

        load_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        logger.info(f"Page load time: {load_time:.2f}ms")

        # Assert reasonable load time (less than 15 seconds)
        assert load_time < 15000, f"Page load time too slow: {load_time:.2f}ms"

        logger.info("✅ Mobile performance test passed")
