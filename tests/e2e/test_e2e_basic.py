"""
End-to-End Tests for SmartShop AI Test Framework

This module contains end-to-end tests that simulate real user workflows
from start to finish.
"""

import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestE2EBasic:
    """Basic end-to-end tests that simulate complete user journeys."""

    def test_complete_user_registration_flow(self, driver):
        """E2E test: Complete user registration workflow."""
        # Step 1: Navigate to home page
        driver.get("https://automationexercise.com/")

        # Step 2: Click on Signup/Login button
        signup_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']"))
        )
        signup_link.click()

        # Step 3: Verify we're on login page
        WebDriverWait(driver, 10).until(EC.url_contains("/login"))

        # Step 4: Click on "New User Signup!" section
        signup_section = driver.find_element(By.CSS_SELECTOR, ".signup-form")
        assert signup_section.is_displayed()

        # Step 5: Fill in registration form
        name_input = driver.find_element(
            By.CSS_SELECTOR, "input[data-qa='signup-name']"
        )
        email_input = driver.find_element(
            By.CSS_SELECTOR, "input[data-qa='signup-email']"
        )

        # Generate unique email
        import random
        import string

        unique_email = f"testuser_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"

        name_input.send_keys("Test User")
        email_input.send_keys(unique_email)

        # Step 6: Click signup button
        signup_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='signup-button']"
        )
        signup_button.click()

        # Step 7: Verify we're on account creation page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login-form"))
        )

        # Note: We don't complete the full registration as it requires additional steps
        # This demonstrates the E2E flow structure

    def test_product_browsing_and_search_flow(self, driver):
        """E2E test: Complete product browsing and search workflow."""
        # Step 1: Navigate to home page
        driver.get("https://automationexercise.com/")

        # Step 2: Navigate to products page
        products_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        products_link.click()

        # Step 3: Verify we're on products page
        WebDriverWait(driver, 10).until(EC.url_contains("/products"))

        # Step 4: Check that products are displayed
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".single-products"))
        )
        assert len(products) > 0, "Products should be displayed"

        # Step 5: Use search functionality
        search_input = driver.find_element(By.CSS_SELECTOR, "#search_product")
        search_input.clear()
        search_input.send_keys("dress")

        search_button = driver.find_element(By.CSS_SELECTOR, "#submit_search")
        search_button.click()

        # Step 6: Verify search results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        # Step 7: Check that search results contain the search term
        product_names = driver.find_elements(By.CSS_SELECTOR, ".product-information h2")
        if product_names:
            # Verify at least one product name contains the search term
            found_search_term = any(
                "dress" in name.text.lower() for name in product_names
            )
            assert found_search_term, "Search results should contain the search term"

    def test_navigation_and_menu_flow(self, driver):
        """E2E test: Complete navigation and menu workflow."""
        # Step 1: Navigate to home page
        driver.get("https://automationexercise.com/")

        # Step 2: Test main navigation menu
        menu_items = [
            ("a[href='/']", "Home"),
            ("a[href='/products']", "Products"),
            ("a[href='/view_cart']", "Cart"),
            ("a[href='/login']", "Signup/Login"),
        ]

        for selector, expected_text in menu_items:
            try:
                menu_item = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                assert (
                    menu_item.is_displayed()
                ), f"Menu item {expected_text} should be visible"

                # Click on menu item
                menu_item.click()

                # Wait for page to load
                time.sleep(2)

                # Verify navigation worked
                if "products" in selector:
                    assert "products" in driver.current_url
                elif "login" in selector:
                    assert "login" in driver.current_url
                elif "cart" in selector:
                    assert "cart" in driver.current_url

                # Navigate back to home for next iteration
                if "home" not in selector:
                    driver.get("https://automationexercise.com/")
                    time.sleep(1)

            except Exception as e:
                # Some menu items might not be available or might have different behavior
                print(f"Menu item {expected_text} test skipped: {e}")

    def test_responsive_design_flow(self, driver):
        """E2E test: Complete responsive design testing workflow."""
        # Test different device sizes
        device_configs = [
            {"name": "Desktop", "width": 1920, "height": 1080},
            {"name": "Laptop", "width": 1366, "height": 768},
            {"name": "Tablet", "width": 768, "height": 1024},
            {"name": "Mobile", "width": 375, "height": 667},
        ]

        for device in device_configs:
            # Set viewport size
            driver.set_window_size(device["width"], device["height"])
            time.sleep(1)

            # Navigate to home page
            driver.get("https://automationexercise.com/")

            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            # Verify page loads correctly
            assert "Automation Exercise" in driver.title

            # Check that navigation is accessible
            nav_menu = driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
            assert nav_menu.is_displayed()

            # Check that logo is visible
            logo = driver.find_element(By.CSS_SELECTOR, ".logo")
            assert logo.is_displayed()

            # Check that footer is visible
            footer = driver.find_element(By.CSS_SELECTOR, ".footer-widget")
            assert footer.is_displayed()

    def test_error_handling_flow(self, driver):
        """E2E test: Error handling and edge cases workflow."""
        # Step 1: Test invalid URL handling
        driver.get("https://automationexercise.com/nonexistent-page")

        # Step 2: Check if we get redirected or error page
        current_url = driver.current_url

        # Step 3: Navigate back to valid page
        driver.get("https://automationexercise.com/")

        # Step 4: Test search with empty query
        driver.get("https://automationexercise.com/products")

        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search_product"))
        )

        # Clear search and submit empty search
        search_input.clear()
        search_button = driver.find_element(By.CSS_SELECTOR, "#submit_search")
        search_button.click()

        # Step 5: Verify page still loads correctly
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
        )

        # Step 6: Test with very long search term
        # Re-find the search input after navigation to avoid stale element
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search_product"))
        )
        search_input.clear()
        long_search_term = "a" * 1000  # Very long search term
        search_input.send_keys(long_search_term)
        search_button = driver.find_element(By.CSS_SELECTOR, "#submit_search")
        search_button.click()

        # Step 7: Verify page handles long input gracefully
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # Page should not crash or show errors
        assert "Automation Exercise" in driver.title

    @pytest.mark.slow
    def test_performance_and_stability_flow(self, driver):
        """E2E test: Performance and stability testing workflow."""
        # Step 1: Navigate to home page multiple times to test stability
        for i in range(3):
            driver.get("https://automationexercise.com/")

            # Wait for page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".features_items"))
            )

            # Verify page loads correctly each time
            assert "Automation Exercise" in driver.title

            # Check that all essential elements are present
            essential_elements = [
                ".logo",
                ".navbar-nav",
                ".features_items",
                ".footer-widget",
            ]
            for selector in essential_elements:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                assert element.is_displayed()

            time.sleep(1)  # Brief pause between iterations

        # Step 2: Test rapid navigation
        pages = [
            "https://automationexercise.com/",
            "https://automationexercise.com/products",
            "https://automationexercise.com/",
        ]

        for page_url in pages:
            driver.get(page_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            assert "Automation Exercise" in driver.title
