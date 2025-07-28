"""
Constants for SmartShop AI Test Framework
"""

# Browser constants
BROWSER_CHROME = "chrome"
BROWSER_FIREFOX = "firefox"
BROWSER_SAFARI = "safari"
BROWSER_EDGE = "edge"

# Test types
TEST_TYPE_UI = "ui"
TEST_TYPE_API = "api"
TEST_TYPE_UNIT = "unit"
TEST_TYPE_INTEGRATION = "integration"
TEST_TYPE_PERFORMANCE = "performance"
TEST_TYPE_VISUAL = "visual"
TEST_TYPE_SMOKE = "smoke"
TEST_TYPE_REGRESSION = "regression"

# Environment types
ENV_DEV = "development"
ENV_STAGING = "staging"
ENV_PROD = "production"
ENV_TEST = "test"

# Timeouts
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 5
LONG_TIMEOUT = 30

# URLs
DEMO_URLS = {
    "automation_exercise": "https://automationexercise.com",
    "the_internet": "https://the-internet.herokuapp.com",
    "nopcommerce": "https://demo.nopcommerce.com",
}

# File paths
SCREENSHOT_DIR = "reports/screenshots"
LOG_DIR = "logs"
REPORT_DIR = "reports"

# AI Configuration
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
DEFAULT_OPENAI_TEMPERATURE = 0.7
DEFAULT_OPENAI_MAX_TOKENS = 1000

# Test data
DEFAULT_USER_TYPE = "customer"
DEFAULT_PRODUCT_CATEGORY = "electronics"
DEFAULT_PRODUCT_COUNT = 10
