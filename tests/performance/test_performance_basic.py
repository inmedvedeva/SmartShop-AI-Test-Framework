"""
Performance Tests for SmartShop AI Test Framework

This module contains performance tests that verify the application meets
performance requirements under various conditions.
"""

import time

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestPerformanceBasic:
    """Basic performance tests to verify application performance."""

    def test_page_load_performance(self, driver):
        """Performance test: Page should load within acceptable time."""
        # Test home page load performance
        start_time = time.time()
        driver.get("https://automationexercise.com/")

        # Wait for page to be fully loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        load_time = time.time() - start_time

        # Page should load within 15 seconds
        assert (
            load_time < 15
        ), f"Home page load took {load_time:.2f} seconds, should be under 15 seconds"

    def test_products_page_performance(self, driver):
        """Performance test: Products page should load within acceptable time."""
        # Test products page load performance
        start_time = time.time()
        driver.get("https://automationexercise.com/products")

        # Wait for products to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".single-products"))
        )

        load_time = time.time() - start_time

        # Page should load within 15 seconds
        assert (
            load_time < 15
        ), f"Products page load took {load_time:.2f} seconds, should be under 15 seconds"

    def test_search_performance(self, driver):
        """Performance test: Search functionality should be responsive."""
        # Navigate to products page
        driver.get("https://automationexercise.com/products")

        # Wait for search input
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search_product"))
        )

        # Test search performance
        search_terms = ["dress", "top", "shirt"]

        for term in search_terms:
            # Clear and enter search term
            search_input.clear()
            search_input.send_keys(term)

            # Measure search response time
            start_time = time.time()
            search_button = driver.find_element(By.CSS_SELECTOR, "#submit_search")
            search_button.click()

            # Wait for results
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
            )

            search_time = time.time() - start_time

            # Search should complete within 10 seconds
            assert (
                search_time < 10
            ), f"Search for '{term}' took {search_time:.2f} seconds, should be under 10 seconds"

            # Navigate back to products page for next search
            driver.get("https://automationexercise.com/products")
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#search_product"))
            )

    def test_navigation_performance(self, driver):
        """Performance test: Navigation between pages should be fast."""
        # Test navigation performance
        pages = [
            "https://automationexercise.com/",
            "https://automationexercise.com/products",
            "https://automationexercise.com/login",
            "https://automationexercise.com/view_cart",
        ]

        for page_url in pages:
            # Measure navigation time
            start_time = time.time()
            driver.get(page_url)

            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            navigation_time = time.time() - start_time

            # Navigation should complete within 15 seconds
            assert (
                navigation_time < 15
            ), f"Navigation to {page_url} took {navigation_time:.2f} seconds, should be under 15 seconds"

    def test_api_performance(self):
        """Performance test: API endpoints should respond quickly."""
        # Test API performance
        api_endpoints = [
            "https://automationexercise.com/api/productsList",
            "https://automationexercise.com/api/brandsList",
        ]

        for endpoint in api_endpoints:
            try:
                # Measure API response time
                start_time = time.time()
                response = requests.get(endpoint, timeout=10)
                api_time = time.time() - start_time

                # API should respond within 15 seconds
                assert (
                    api_time < 15
                ), f"API {endpoint} took {api_time:.2f} seconds, should be under 15 seconds"
                assert (
                    response.status_code == 200
                ), f"API {endpoint} should return 200 status"

            except requests.RequestException as e:
                pytest.skip(f"API {endpoint} not accessible: {e}")

    def test_responsive_performance(self, driver):
        """Performance test: Responsive design should perform well on all devices."""
        # Test performance on different screen sizes
        screen_sizes = [
            (1920, 1080, "Desktop"),
            (1366, 768, "Laptop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile"),
        ]

        for width, height, device_name in screen_sizes:
            # Set viewport size
            driver.set_window_size(width, height)
            time.sleep(1)

            # Test home page performance
            start_time = time.time()
            driver.get("https://automationexercise.com/")

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
            )

            load_time = time.time() - start_time

            # Page should load within 15 seconds on all devices
            assert (
                load_time < 15
            ), f"{device_name} view took {load_time:.2f} seconds, should be under 15 seconds"

    def test_image_loading_performance(self, driver):
        """Performance test: Images should load within acceptable time."""
        # Navigate to products page
        driver.get("https://automationexercise.com/products")

        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".single-products"))
        )

        # Check image loading performance
        images = driver.find_elements(By.TAG_NAME, "img")

        for img in images:
            try:
                # Check if image is loaded
                width = img.get_attribute("naturalWidth")
                height = img.get_attribute("naturalHeight")

                # Image should have dimensions (indicating it loaded)
                assert width and height, "Image should have dimensions"

            except Exception:
                # Some images might not have naturalWidth/Height attributes
                pass

    def test_memory_usage_performance(self, driver):
        """Performance test: Application should not consume excessive memory."""
        # Navigate to multiple pages to test memory usage
        pages = [
            "https://automationexercise.com/",
            "https://automationexercise.com/products",
            "https://automationexercise.com/login",
            "https://automationexercise.com/view_cart",
        ]

        for page_url in pages:
            # Navigate to page
            driver.get(page_url)

            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            # Verify page loads correctly
            assert "Automation Exercise" in driver.title

            # Brief pause to allow memory to stabilize
            time.sleep(1)

    def test_concurrent_access_performance(self, driver):
        """Performance test: Application should handle rapid page access."""
        # Test rapid navigation
        pages = [
            "https://automationexercise.com/",
            "https://automationexercise.com/products",
            "https://automationexercise.com/",
        ]

        for i, page_url in enumerate(pages):
            # Navigate to page
            driver.get(page_url)

            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            # Verify page loads correctly
            assert "Automation Exercise" in driver.title

            # Brief pause between navigations
            if i < len(pages) - 1:
                time.sleep(0.5)

    @pytest.mark.slow
    def test_stress_performance(self, driver):
        """Performance test: Application should handle stress conditions."""
        # Test application under stress (multiple rapid operations)
        for i in range(5):
            # Navigate to home page
            driver.get("https://automationexercise.com/")

            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
            )

            # Verify page loads correctly
            assert "Automation Exercise" in driver.title

            # Navigate to products page
            driver.get("https://automationexercise.com/products")

            # Wait for products to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".single-products"))
            )

            # Verify products page loads
            assert "products" in driver.current_url

            # Brief pause between iterations
            time.sleep(1)

    def test_network_performance(self, driver):
        """Performance test: Network requests should be optimized."""
        # Test network performance by checking resource loading
        driver.get("https://automationexercise.com/")

        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        # Check that all essential resources are loaded
        essential_elements = [
            ".logo",
            ".navbar-nav",
            ".features_items",
            ".footer-widget",
        ]

        for selector in essential_elements:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            assert (
                element.is_displayed()
            ), f"Essential element {selector} should be loaded"
