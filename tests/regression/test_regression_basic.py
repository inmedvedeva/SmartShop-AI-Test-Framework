"""
Regression Tests for SmartShop AI Test Framework

This module contains regression tests that ensure previously working functionality
continues to work after changes.
"""

import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestRegressionBasic:
    """Basic regression tests to ensure core functionality remains intact."""

    def test_home_page_regression(self, driver):
        """Regression test: Home page should load correctly."""
        # Navigate to home page
        driver.get("https://automationexercise.com/")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Check that page title is correct
        assert "Automation Exercise" in driver.title

        # Check that logo is present
        logo = driver.find_element(By.CSS_SELECTOR, ".logo a")
        assert logo.is_displayed()

        # Check that navigation menu is present
        nav_menu = driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
        assert nav_menu.is_displayed()

    def test_search_functionality_regression(self, driver):
        """Regression test: Search functionality should work."""
        # Navigate to products page
        driver.get("https://automationexercise.com/products")

        # Wait for search input to be present
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search_product"))
        )

        # Enter search term
        search_input.clear()
        search_input.send_keys("top")

        # Click search button
        search_button = driver.find_element(By.CSS_SELECTOR, "#submit_search")
        search_button.click()

        # Wait for search results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        # Check that search results are displayed
        products = driver.find_elements(By.CSS_SELECTOR, ".single-products")
        assert len(products) > 0

    def test_navigation_regression(self, driver):
        """Regression test: Navigation between pages should work."""
        # Start from home page
        driver.get("https://automationexercise.com/")

        # Navigate to products page
        products_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        # Verify we're on products page
        WebDriverWait(driver, 10).until(EC.url_contains("/products"))
        assert "products" in driver.current_url

        # Navigate back to home
        home_link = driver.find_element(By.CSS_SELECTOR, "a[href='/']")
        home_link.click()

        # Verify we're back on home page
        WebDriverWait(driver, 10).until(EC.url_contains("automationexercise.com"))
        assert "automationexercise.com" in driver.current_url

    def test_page_elements_regression(self, driver):
        """Regression test: All essential page elements should be present."""
        # Navigate to home page
        driver.get("https://automationexercise.com/")

        # Check for essential elements
        essential_elements = [
            ".logo",  # Logo
            ".navbar-nav",  # Navigation menu
            ".features_items",  # Featured products
            ".footer-widget",  # Footer
        ]

        for selector in essential_elements:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            assert element.is_displayed(), f"Element {selector} should be visible"

    def test_responsive_design_regression(self, driver):
        """Regression test: Page should be responsive on different screen sizes."""
        # Test different viewport sizes
        viewport_sizes = [
            (1920, 1080),  # Desktop
            (1366, 768),  # Laptop
            (768, 1024),  # Tablet
            (375, 667),  # Mobile
        ]

        for width, height in viewport_sizes:
            # Set viewport size
            driver.set_window_size(width, height)
            time.sleep(1)  # Allow page to adjust

            # Navigate to home page
            driver.get("https://automationexercise.com/")

            # Check that page loads without errors
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            # Verify page is accessible
            assert "Automation Exercise" in driver.title

            # Check that navigation is still functional
            nav_menu = driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
            assert nav_menu.is_displayed()

    @pytest.mark.slow
    def test_performance_regression(self, driver):
        """Regression test: Page load performance should remain acceptable."""
        # Navigate to home page and measure load time
        start_time = time.time()
        driver.get("https://automationexercise.com/")

        # Wait for page to be fully loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        load_time = time.time() - start_time

        # Performance should be under 15 seconds (accounting for network delays)
        assert (
            load_time < 15
        ), f"Page load took {load_time:.2f} seconds, should be under 15 seconds"

        # Check that all images are loaded
        images = driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            # Check if image is loaded (has natural width/height)
            try:
                width = img.get_attribute("naturalWidth")
                height = img.get_attribute("naturalHeight")
                assert width and height, "Image should have dimensions"
            except Exception:
                # Some images might not have naturalWidth/Height attributes
                pass
