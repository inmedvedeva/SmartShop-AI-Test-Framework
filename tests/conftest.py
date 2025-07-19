"""
Pytest configuration and fixtures for SmartShop AI Test Framework
"""

import time

import pytest
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.settings import settings


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default=settings.browser,
        help="Browser to use for tests (chrome, firefox, edge)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=settings.headless,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--url", action="store", default=settings.base_url, help="Base URL for testing"
    )


@pytest.fixture(scope="session")
def browser_type(request):
    """Get browser type from command line"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode from command line"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def base_url(request):
    """Get base URL from command line"""
    return request.config.getoption("--url")


@pytest.fixture(scope="function")
def driver(browser_type, headless_mode, base_url):
    """
    WebDriver fixture that provides a browser instance for each test
    """
    driver = None

    try:
        if browser_type.lower() == "chrome":
            driver = _setup_chrome_driver(headless_mode)
        elif browser_type.lower() == "firefox":
            driver = _setup_firefox_driver(headless_mode)
        elif browser_type.lower() == "edge":
            driver = _setup_edge_driver(headless_mode)
        else:
            logger.warning(f"Unsupported browser: {browser_type}, using Chrome")
            driver = _setup_chrome_driver(headless_mode)

        # Set window size
        driver.set_window_size(1920, 1080)

        # Set implicit wait
        driver.implicitly_wait(settings.implicit_wait)

        # Set page load timeout
        driver.set_page_load_timeout(settings.browser_timeout)

        logger.info(
            f"✅ WebDriver initialized: {browser_type} (headless: {headless_mode})"
        )

        yield driver

    except Exception as e:
        logger.error(f"❌ Failed to initialize WebDriver: {e}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("✅ WebDriver closed")
            except Exception as e:
                logger.warning(f"⚠️ Error closing WebDriver: {e}")


def _setup_chrome_driver(headless_mode):
    """Setup Chrome WebDriver"""
    options = Options()

    if headless_mode:
        options.add_argument("--headless")

    # Additional Chrome options for stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Speed up tests

    # Set user agent
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    try:
        # Try to use webdriver-manager for automatic driver management
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        logger.warning(f"Failed to use webdriver-manager: {e}")
        # Fallback to system Chrome driver
        driver = webdriver.Chrome(options=options)

    return driver


def _setup_firefox_driver(headless_mode):
    """Setup Firefox WebDriver"""
    options = FirefoxOptions()

    if headless_mode:
        options.add_argument("--headless")

    # Additional Firefox options
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.add_argument("--disable-extensions")

    try:
        # Try to use webdriver-manager for automatic driver management
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    except Exception as e:
        logger.warning(f"Failed to use webdriver-manager: {e}")
        # Fallback to system Firefox driver
        driver = webdriver.Firefox(options=options)

    return driver


def _setup_edge_driver(headless_mode):
    """Setup Edge WebDriver"""
    try:
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        options = EdgeOptions()

        if headless_mode:
            options.add_argument("--headless")

        # Additional Edge options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        except Exception as e:
            logger.warning(f"Failed to use webdriver-manager: {e}")
            driver = webdriver.Edge(options=options)

        return driver
    except ImportError:
        logger.error("Edge WebDriver not available, falling back to Chrome")
        return _setup_chrome_driver(headless_mode)


@pytest.fixture(scope="function")
def ai_generator():
    """AI Data Generator fixture"""
    from utils.ai_data_generator import AIDataGenerator

    return AIDataGenerator()


@pytest.fixture(scope="function")
def visual_tester():
    """Visual Tester fixture"""
    from utils.visual_testing import VisualTester

    return VisualTester()


# Pytest markers registration
def pytest_configure(config):
    """Register custom pytest markers"""
    markers = [
        "ui: marks tests as UI tests",
        "api: marks tests as API tests",
        "smoke: marks tests as smoke tests",
        "regression: marks tests as regression tests",
        "performance: marks tests as performance tests",
        "visual: marks tests as visual tests",
        "ai: marks tests as AI-powered tests",
        "slow: marks tests as slow running tests",
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)


# Test result hooks
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs.get("driver")
            if driver:
                # Take screenshot
                timestamp = int(time.time())
                screenshot_name = f"failure_{item.name}_{timestamp}.png"
                screenshot_path = f"./reports/screenshots/{screenshot_name}"

                # Ensure screenshots directory exists
                import os

                os.makedirs("./reports/screenshots", exist_ok=True)

                driver.save_screenshot(screenshot_path)
                logger.info(f"📸 Screenshot saved: {screenshot_path}")

                # Add screenshot path to test report
                if hasattr(rep, "extras"):
                    rep.extras.append(pytest_html.extras.image(screenshot_path))

        except Exception as e:
            logger.warning(f"Failed to capture screenshot: {e}")


# Test session hooks
def pytest_sessionstart(session):
    """Actions to perform at the start of test session"""
    logger.info("🚀 Starting test session")
    logger.info(f"📊 Test configuration:")
    logger.info(f"   • Browser: {session.config.getoption('--browser')}")
    logger.info(f"   • Headless: {session.config.getoption('--headless')}")
    logger.info(f"   • Base URL: {session.config.getoption('--url')}")


def pytest_sessionfinish(session, exitstatus):
    """Actions to perform at the end of test session"""
    logger.info("🏁 Test session finished")
    logger.info(f"📈 Exit status: {exitstatus}")

    # Print summary
    if hasattr(session, "testscollected"):
        logger.info(f"📋 Tests collected: {session.testscollected}")

    # Note: Detailed test results are shown in the test output above
    logger.info("📊 Test session completed")
