"""
Smoke Tests for SmartShop AI Test Framework

This module contains smoke tests that verify the most critical functionality
is working before running more comprehensive test suites.
"""

import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestSmokeBasic:
    """Basic smoke tests to verify critical functionality is working."""

    def test_home_page_smoke(self, driver):
        """Smoke test: Home page should load and display basic elements."""
        # Navigate to home page
        driver.get("https://automationexercise.com/")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Critical checks
        assert "Automation Exercise" in driver.title, "Page title should be correct"

        # Check that logo is present
        logo = driver.find_element(By.CSS_SELECTOR, ".logo a")
        assert logo.is_displayed(), "Logo should be visible"

        # Check that navigation menu is present
        nav_menu = driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
        assert nav_menu.is_displayed(), "Navigation menu should be visible"

    def test_products_page_smoke(self, driver):
        """Smoke test: Products page should load and display products."""
        # Navigate to products page
        driver.get("https://automationexercise.com/products")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Critical checks
        assert "products" in driver.current_url, "Should be on products page"

        # Check that products are displayed
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".single-products"))
        )
        assert len(products) > 0, "Products should be displayed"

        # Check that search functionality is available
        search_input = driver.find_element(By.CSS_SELECTOR, "#search_product")
        assert search_input.is_displayed(), "Search input should be visible"

    def test_navigation_smoke(self, driver):
        """Smoke test: Basic navigation should work."""
        # Start from home page
        driver.get("https://automationexercise.com/")

        # Navigate to products page
        products_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        # Verify navigation worked
        WebDriverWait(driver, 10).until(EC.url_contains("/products"))
        assert "products" in driver.current_url, "Should navigate to products page"

        # Navigate back to home
        home_link = driver.find_element(By.CSS_SELECTOR, "a[href='/']")
        home_link.click()

        # Verify we're back on home page
        WebDriverWait(driver, 10).until(EC.url_contains("automationexercise.com"))
        assert (
            "automationexercise.com" in driver.current_url
        ), "Should navigate back to home"

    def test_search_functionality_smoke(self, driver):
        """Smoke test: Search functionality should work."""
        # Navigate to products page
        driver.get("https://automationexercise.com/products")

        # Wait for search input
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search_product"))
        )

        # Perform search
        search_input.clear()
        search_input.send_keys("top")

        search_button = driver.find_element(By.CSS_SELECTOR, "#submit_search")
        search_button.click()

        # Verify search results page loads
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        # Check that search results are displayed
        products = driver.find_elements(By.CSS_SELECTOR, ".single-products")
        assert len(products) > 0, "Search should return results"

    def test_login_page_smoke(self, driver):
        """Smoke test: Login page should load correctly."""
        # Navigate to login page
        driver.get("https://automationexercise.com/login")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Critical checks
        assert "login" in driver.current_url, "Should be on login page"

        # Check that login form is present
        login_form = driver.find_element(By.CSS_SELECTOR, ".login-form")
        assert login_form.is_displayed(), "Login form should be visible"

        # Check that signup form is present
        signup_form = driver.find_element(By.CSS_SELECTOR, ".signup-form")
        assert signup_form.is_displayed(), "Signup form should be visible"

    def test_cart_page_smoke(self, driver):
        """Smoke test: Cart page should load correctly."""
        # Navigate to cart page
        driver.get("https://automationexercise.com/view_cart")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Critical checks
        assert "cart" in driver.current_url, "Should be on cart page"

        # Check that cart page loads without errors
        assert "Automation Exercise" in driver.title, "Page should load correctly"

    def test_responsive_smoke(self, driver):
        """Smoke test: Page should be responsive on different screen sizes."""
        # Test desktop size
        driver.set_window_size(1920, 1080)
        driver.get("https://automationexercise.com/")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        assert "Automation Exercise" in driver.title, "Desktop view should work"

        # Test mobile size
        driver.set_window_size(375, 667)
        driver.get("https://automationexercise.com/")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        assert "Automation Exercise" in driver.title, "Mobile view should work"

    def test_performance_smoke(self, driver):
        """Smoke test: Page should load within acceptable time."""
        # Measure page load time
        start_time = time.time()
        driver.get("https://automationexercise.com/")

        # Wait for page to be fully loaded
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        load_time = time.time() - start_time

        # Page should load within 15 seconds
        assert (
            load_time < 15
        ), f"Page load took {load_time:.2f} seconds, should be under 15 seconds"

    def test_error_handling_smoke(self, driver):
        """Smoke test: Application should handle errors gracefully."""
        # Test invalid URL
        driver.get("https://automationexercise.com/nonexistent-page")

        # Should not crash, should either redirect or show error page
        current_url = driver.current_url

        # Navigate back to valid page
        driver.get("https://automationexercise.com/")

        # Should load correctly after error
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        assert (
            "Automation Exercise" in driver.title
        ), "Should recover from error gracefully"
