"""
Browser management utilities for SmartShop AI Test Framework
"""

import os

from loguru import logger
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.core.constants import (
    BROWSER_CHROME,
    BROWSER_EDGE,
    BROWSER_FIREFOX,
    BROWSER_SAFARI,
    DEFAULT_TIMEOUT,
)


class BrowserManager:
    """Browser management class"""

    def __init__(self, browser_type=BROWSER_CHROME, headless=True):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.driver = None
        self.playwright = None
        self.browser = None
        self.page = None

    def get_selenium_driver(self):
        """Get Selenium WebDriver instance"""
        try:
            if self.browser_type == BROWSER_CHROME:
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")

                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)

            elif self.browser_type == BROWSER_FIREFOX:
                options = webdriver.FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")

                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)

            else:
                raise ValueError(f"Unsupported browser: {self.browser_type}")

            self.driver.implicitly_wait(DEFAULT_TIMEOUT)
            self.driver.maximize_window()
            logger.info(f"Selenium {self.browser_type} driver initialized")
            return self.driver

        except Exception as e:
            logger.error(f"Failed to initialize Selenium driver: {e}")
            raise

    def get_playwright_browser(self):
        """Get Playwright browser instance"""
        try:
            self.playwright = sync_playwright().start()

            if self.browser_type == BROWSER_CHROME:
                self.browser = self.playwright.chromium.launch(
                    headless=self.headless,
                    args=["--no-sandbox", "--disable-dev-shm-usage"],
                )
            elif self.browser_type == BROWSER_FIREFOX:
                self.browser = self.playwright.firefox.launch(headless=self.headless)
            elif self.browser_type == BROWSER_SAFARI:
                self.browser = self.playwright.webkit.launch(headless=self.headless)
            else:
                raise ValueError(f"Unsupported browser: {self.browser_type}")

            self.page = self.browser.new_page()
            self.page.set_viewport_size({"width": 1920, "height": 1080})
            logger.info(f"Playwright {self.browser_type} browser initialized")
            return self.browser, self.page

        except Exception as e:
            logger.error(f"Failed to initialize Playwright browser: {e}")
            raise

    def close_selenium_driver(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Selenium driver closed")

    def close_playwright_browser(self):
        """Close Playwright browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.browser = None
        self.page = None
        self.playwright = None
        logger.info("Playwright browser closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_selenium_driver()
        self.close_playwright_browser()


def get_browser_manager(browser_type=None, headless=None):
    """Factory function to get browser manager"""
    if browser_type is None:
        browser_type = os.getenv("BROWSER", BROWSER_CHROME)

    if headless is None:
        headless = os.getenv("HEADLESS", "true").lower() == "true"

    return BrowserManager(browser_type=browser_type, headless=headless)
