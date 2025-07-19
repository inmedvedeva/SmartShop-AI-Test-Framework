"""
Constants used throughout the test framework
"""

from selenium.webdriver.common.by import By

# Common URLs
BASE_URL = "https://automationexercise.com"
API_BASE_URL = "https://automationexercise.com/api"
ADMIN_URL = "https://automationexercise.com"

# Common locators
COMMON_LOCATORS = {
    "page_title": (By.TAG_NAME, "title"),
    "body": (By.TAG_NAME, "body"),
    "loading_spinner": (By.CLASS_NAME, "loading"),
    "error_message": (By.CLASS_NAME, "error"),
    "success_message": (By.CLASS_NAME, "success"),
    "modal_overlay": (By.CLASS_NAME, "modal-overlay"),
    "close_button": (By.CLASS_NAME, "close"),
    "submit_button": (By.CSS_SELECTOR, "button[type='submit']"),
    "cancel_button": (By.CSS_SELECTOR, "button[type='button']"),
}

# Form field locators
FORM_LOCATORS = {
    "email_input": (By.CSS_SELECTOR, "input[type='email']"),
    "password_input": (By.CSS_SELECTOR, "input[type='password']"),
    "text_input": (By.CSS_SELECTOR, "input[type='text']"),
    "number_input": (By.CSS_SELECTOR, "input[type='number']"),
    "checkbox": (By.CSS_SELECTOR, "input[type='checkbox']"),
    "radio_button": (By.CSS_SELECTOR, "input[type='radio']"),
    "select_dropdown": (By.TAG_NAME, "select"),
    "textarea": (By.TAG_NAME, "textarea"),
}

# Navigation locators
NAVIGATION_LOCATORS = {
    "home_link": (By.CSS_SELECTOR, "a[href='/']"),
    "products_link": (By.CSS_SELECTOR, "a[href='/products']"),
    "cart_link": (By.CSS_SELECTOR, "a[href='/cart']"),
    "login_link": (By.CSS_SELECTOR, "a[href='/login']"),
    "register_link": (By.CSS_SELECTOR, "a[href='/register']"),
    "logout_link": (By.CSS_SELECTOR, "a[href='/logout']"),
    "profile_link": (By.CSS_SELECTOR, "a[href='/profile']"),
    "admin_link": (By.CSS_SELECTOR, "a[href='/admin']"),
}

# User types
USER_TYPES = {
    "customer": "customer",
    "admin": "admin",
    "vendor": "vendor",
    "guest": "guest",
}

# Product categories
PRODUCT_CATEGORIES = {
    "electronics": "electronics",
    "clothing": "clothing",
    "books": "books",
    "home": "home",
    "sports": "sports",
    "beauty": "beauty",
    "automotive": "automotive",
    "toys": "toys",
}

# Test data constants
TEST_DATA = {
    "default_email": "test@smartshop.com",
    "default_password": "TestPassword123!",
    "admin_email": "admin@smartshop.com",
    "admin_password": "AdminPassword123!",
    "test_user_name": "Test User",
    "test_company": "Test Company",
    "test_address": "123 Test Street",
    "test_city": "Test City",
    "test_country": "Test Country",
    "test_zipcode": "12345",
    "test_phone": "+1234567890",
}

# API endpoints
API_ENDPOINTS = {
    "products": "/products",
    "users": "/users",
    "orders": "/orders",
    "cart": "/cart",
    "auth": "/auth",
    "search": "/search",
    "categories": "/categories",
    "reviews": "/reviews",
}

# HTTP status codes
HTTP_STATUS_CODES = {
    "ok": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "method_not_allowed": 405,
    "conflict": 409,
    "unprocessable_entity": 422,
    "internal_server_error": 500,
    "service_unavailable": 503,
}

# Browser types
BROWSER_TYPES = {
    "chrome": "chrome",
    "firefox": "firefox",
    "safari": "safari",
    "edge": "edge",
}

# Test markers
TEST_MARKERS = {
    "smoke": "smoke",
    "regression": "regression",
    "ui": "ui",
    "api": "api",
    "integration": "integration",
    "performance": "performance",
    "visual": "visual",
    "slow": "slow",
    "flaky": "flaky",
}

# Timeouts (in seconds)
TIMEOUTS = {
    "implicit_wait": 10,
    "explicit_wait": 30,
    "page_load": 60,
    "script_timeout": 30,
    "api_timeout": 30,
    "visual_timeout": 10,
}

# File paths
FILE_PATHS = {
    "screenshots": "./reports/screenshots",
    "allure_results": "./reports/allure-results",
    "allure_report": "./reports/allure-report",
    "html_reports": "./reports/html",
    "logs": "./reports/logs",
    "test_data": "./data",
    "config": "./config",
}

# Log messages
LOG_MESSAGES = {
    "test_started": "Test started: {}",
    "test_passed": "Test passed: {}",
    "test_failed": "Test failed: {}",
    "test_skipped": "Test skipped: {}",
    "page_loaded": "Page loaded successfully: {}",
    "element_found": "Element found: {}",
    "element_not_found": "Element not found: {}",
    "click_successful": "Successfully clicked element: {}",
    "input_successful": "Successfully entered text: {}",
    "api_call_successful": "API call successful: {}",
    "api_call_failed": "API call failed: {}",
    "ai_generation_successful": "AI generation successful: {}",
    "ai_generation_failed": "AI generation failed, using Faker: {}",
    "fallback_to_faker": "Falling back to Faker for: {}",
}

# Error messages
ERROR_MESSAGES = {
    "element_not_visible": "Element is not visible: {}",
    "element_not_clickable": "Element is not clickable: {}",
    "page_not_loaded": "Page failed to load: {}",
    "timeout_error": "Timeout error: {}",
    "api_error": "API error: {}",
    "validation_error": "Validation error: {}",
    "configuration_error": "Configuration error: {}",
    "ai_service_error": "AI service error: {}",
}

# Success messages
SUCCESS_MESSAGES = {
    "login_successful": "Login successful",
    "registration_successful": "Registration successful",
    "product_added": "Product added to cart",
    "order_placed": "Order placed successfully",
    "profile_updated": "Profile updated successfully",
    "search_successful": "Search completed successfully",
    "payment_successful": "Payment processed successfully",
}

# Validation messages
VALIDATION_MESSAGES = {
    "email_required": "Email is required",
    "password_required": "Password is required",
    "invalid_email": "Invalid email format",
    "password_too_short": "Password must be at least 8 characters",
    "passwords_dont_match": "Passwords do not match",
    "required_field": "This field is required",
    "invalid_format": "Invalid format",
}

# AI prompts
AI_PROMPTS = {
    "user_profile": "Generate a realistic user profile for a {} user with the following fields: first_name, last_name, email, phone, address, city, country, postal_code, date_of_birth, preferences (list), loyalty_points (integer), registration_date. Return as JSON.",
    "product_catalog": "Generate {} realistic products for the {} category with the following fields: name, description, price (float), currency, category, brand, sku, stock_quantity (integer), rating (float), features (list), images (list of URLs). Return as JSON array.",
    "search_terms": "Generate {} realistic search terms that a user might use to find products in an e-commerce store. Return as JSON array of strings.",
    "test_scenarios": "Generate realistic test scenarios for {} functionality with the following fields: title, description, steps (list), expected_result, priority (high/medium/low), tags (list). Return as JSON array.",
}

# OpenAI error codes
OPENAI_ERROR_CODES = {
    "geographic_restriction": "unsupported_country_region_territory",
    "invalid_api_key": "invalid_api_key",
    "rate_limit": "rate_limit_exceeded",
    "quota_exceeded": "quota_exceeded",
    "model_not_found": "model_not_found",
    "invalid_request": "invalid_request",
}

# Test environment names
ENVIRONMENTS = {
    "development": "development",
    "staging": "staging",
    "production": "production",
    "testing": "testing",
}

# Notification channels
NOTIFICATION_CHANNELS = {
    "email": "email",
    "slack": "slack",
    "teams": "teams",
    "webhook": "webhook",
}

# Report formats
REPORT_FORMATS = {
    "allure": "allure",
    "html": "html",
    "json": "json",
    "xml": "xml",
    "csv": "csv",
}

# Security scan types
SECURITY_SCAN_TYPES = {
    "bandit": "bandit",
    "safety": "safety",
    "snyk": "snyk",
    "owasp": "owasp",
}

# Performance metrics
PERFORMANCE_METRICS = {
    "response_time": "response_time",
    "throughput": "throughput",
    "error_rate": "error_rate",
    "cpu_usage": "cpu_usage",
    "memory_usage": "memory_usage",
    "disk_usage": "disk_usage",
}
