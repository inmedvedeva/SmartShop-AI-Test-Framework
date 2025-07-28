"""
UI helper utilities for SmartShop AI Test Framework
"""

import time
from typing import Optional, Tuple

from loguru import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.core.constants import DEFAULT_TIMEOUT, SHORT_TIMEOUT


class UIHelpers:
    """UI helper methods for Selenium WebDriver"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        self.short_wait = WebDriverWait(driver, SHORT_TIMEOUT)
        self.actions = ActionChains(driver)

    def wait_for_element(
        self, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """Wait for element to be present and visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Element found: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element not found within {timeout}s: {locator}")
            return False

    def wait_for_element_clickable(
        self, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """Wait for element to be clickable"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"Element clickable: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element not clickable within {timeout}s: {locator}")
            return False

    def find_element(self, locator: tuple[str, str]):
        """Find element with explicit wait"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator: tuple[str, str]):
        """Find elements with explicit wait"""
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []

    def click_element(
        self, locator: tuple[str, str], timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """Click element with wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"Clicked element: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Failed to click element: {locator}")
            return False

    def input_text(
        self, locator: tuple[str, str], text: str, clear_first: bool = True
    ) -> bool:
        """Input text into element"""
        try:
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Input text '{text}' into: {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to input text: {locator} - {e}")
            return False

    def get_text(self, locator: tuple[str, str]) -> str | None:
        """Get text from element"""
        try:
            element = self.find_element(locator)
            text = element.text
            logger.info(f"Got text '{text}' from: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text: {locator} - {e}")
            return None

    def get_attribute(self, locator: tuple[str, str], attribute: str) -> str | None:
        """Get attribute value from element"""
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            logger.info(f"Got attribute '{attribute}={value}' from: {locator}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute: {locator} - {e}")
            return None

    def is_element_present(
        self, locator: tuple[str, str], timeout: int = SHORT_TIMEOUT
    ) -> bool:
        """Check if element is present"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_visible(
        self, locator: tuple[str, str], timeout: int = SHORT_TIMEOUT
    ) -> bool:
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator: tuple[str, str]) -> bool:
        """Scroll to element"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Small delay for scroll animation
            logger.info(f"Scrolled to element: {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll to element: {locator} - {e}")
            return False

    def hover_over_element(self, locator: tuple[str, str]) -> bool:
        """Hover over element"""
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            logger.info(f"Hovered over element: {locator}")
            return True
        except Exception as e:
            logger.error(f"Failed to hover over element: {locator} - {e}")
            return False

    def wait_for_page_load(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            logger.info("Page loaded completely")
            return True
        except TimeoutException:
            logger.warning("Page load timeout")
            return False

    def wait_for_url_change(
        self, current_url: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """Wait for URL to change"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != current_url
            )
            logger.info(f"URL changed from {current_url} to {self.driver.current_url}")
            return True
        except TimeoutException:
            logger.warning("URL change timeout")
            return False

    def take_screenshot(self, filename: str | None = None) -> str | None:
        """Take screenshot"""
        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"

            screenshot_path = f"reports/screenshots/{filename}"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None

    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title

    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_load()
        logger.info("Page refreshed")


def get_ui_helpers(driver):
    """Factory function to get UI helpers"""
    return UIHelpers(driver)
