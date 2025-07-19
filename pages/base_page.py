"""
Base class for Page Object Model
"""

import time
from typing import Any, List, Optional

from loguru import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class BasePage:
    """Base class for all pages"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.browser_timeout)
        self.base_url = settings.base_url

    def open(self, url: str = "") -> None:
        """
        Opens a page

        Args:
            url: Additional URL path
        """
        full_url = f"{self.base_url}/{url.lstrip('/')}" if url else self.base_url
        logger.info(f"Opening page: {full_url}")
        self.driver.get(full_url)

    def get_title(self) -> str:
        """Gets page title"""
        return self.driver.title

    def get_current_url(self) -> str:
        """Gets current URL"""
        return self.driver.current_url

    def find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Finds element with wait

        Args:
            locator: Element locator (By, value)
            timeout: Wait timeout

        Returns:
            WebElement
        """
        wait_time = timeout or settings.browser_timeout
        wait = WebDriverWait(self.driver, wait_time)

        try:
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator: tuple, timeout: int = None) -> list[WebElement]:
        """
        Finds all elements with wait

        Args:
            locator: Elements locator (By, value)
            timeout: Wait timeout

        Returns:
            List[WebElement]
        """
        wait_time = timeout or settings.browser_timeout
        wait = WebDriverWait(self.driver, wait_time)

        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"Found {len(elements)} elements for {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []

    def click_element(self, locator: tuple, timeout: int = None) -> None:
        """
        Clicks on element with clickable wait

        Args:
            locator: Element locator
            timeout: Wait timeout
        """
        wait_time = timeout or settings.browser_timeout
        wait = WebDriverWait(self.driver, wait_time)

        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.debug(f"Clicked on element: {locator}")
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise

    def input_text(
        self, locator: tuple, text: str, clear: bool = True, timeout: int = None
    ) -> None:
        """
        Inputs text into field

        Args:
            locator: Field locator
            text: Text to input
            clear: Whether to clear field before input
            timeout: Wait timeout
        """
        element = self.find_element(locator, timeout)

        if clear:
            element.clear()

        element.send_keys(text)
        logger.debug(f"Text entered in {locator}: {text}")

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Gets element text

        Args:
            locator: Element locator
            timeout: Wait timeout

        Returns:
            Element text
        """
        element = self.find_element(locator, timeout)
        text = element.text
        logger.debug(f"Got text from {locator}: {text}")
        return text

    def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """
        Gets element attribute

        Args:
            locator: Element locator
            attribute: Attribute name
            timeout: Wait timeout

        Returns:
            Attribute value
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute {attribute} from {locator}: {value}")
        return value

    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Checks element presence

        Args:
            locator: Element locator
            timeout: Wait timeout

        Returns:
            True if element is present
        """
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Checks element visibility

        Args:
            locator: Element locator
            timeout: Wait timeout

        Returns:
            True if element is visible
        """
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_visible(
        self, locator: tuple, timeout: int = None
    ) -> WebElement:
        """
        Waits for element visibility

        Args:
            locator: Element locator
            timeout: Wait timeout

        Returns:
            WebElement
        """
        wait_time = timeout or settings.browser_timeout
        wait = WebDriverWait(self.driver, wait_time)

        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element became visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element did not become visible: {locator}")
            raise

    def wait_for_element_invisible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Waits for element invisibility

        Args:
            locator: Element locator
            timeout: Wait timeout

        Returns:
            True if element disappeared
        """
        wait_time = timeout or settings.browser_timeout
        wait = WebDriverWait(self.driver, wait_time)

        try:
            wait.until(EC.invisibility_of_element_located(locator))
            logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Element did not disappear: {locator}")
            return False

    def scroll_to_element(self, locator: tuple) -> None:
        """
        Scrolls to element

        Args:
            locator: Element locator
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small pause for scroll completion
        logger.debug(f"Scrolled to element: {locator}")

    def scroll_to_bottom(self) -> None:
        """Scrolls page down"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        logger.debug("Scrolled page down")

    def scroll_to_top(self) -> None:
        """Scrolls page up"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        logger.debug("Scrolled page up")

    def take_screenshot(self, filename: str = None) -> str:
        """
        Takes page screenshot

        Args:
            filename: File name (optional)

        Returns:
            Screenshot file path
        """
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = f"{settings.screenshot_dir}/{filename}"
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def wait_for_page_load(self, timeout: int = None) -> None:
        """
        Waits for page load

        Args:
            timeout: Wait timeout
        """
        wait_time = timeout or settings.browser_timeout
        wait = WebDriverWait(self.driver, wait_time)

        try:
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            logger.debug("Page loaded")
        except TimeoutException:
            logger.warning("Page load timeout")

    def refresh_page(self) -> None:
        """Refreshes the page"""
        self.driver.refresh()
        self.wait_for_page_load()
        logger.debug("Page refreshed")

    def go_back(self) -> None:
        """Goes back to previous page"""
        self.driver.back()
        self.wait_for_page_load()
        logger.debug("Went back to previous page")

    def go_forward(self) -> None:
        """Goes forward to next page"""
        self.driver.forward()
        self.wait_for_page_load()
        logger.debug("Went forward to next page")

    def accept_alert(self) -> None:
        """Accepts alert"""
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            logger.debug("Alert accepted")
        except Exception as e:
            logger.warning(f"No alert to accept: {e}")

    def dismiss_alert(self) -> None:
        """Dismisses alert"""
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            logger.debug("Alert dismissed")
        except Exception as e:
            logger.warning(f"No alert to dismiss: {e}")

    def get_alert_text(self) -> str:
        """Gets alert text"""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            logger.debug(f"Alert text: {text}")
            return text
        except Exception as e:
            logger.warning(f"No alert to get text from: {e}")
            return ""

    def switch_to_frame(self, frame_locator) -> None:
        """
        Switches to iframe

        Args:
            frame_locator: iframe locator
        """
        try:
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
            logger.debug(f"Switched to iframe: {frame_locator}")
        except Exception as e:
            logger.error(f"Error switching to iframe: {e}")
            raise

    def switch_to_default_content(self) -> None:
        """Switches to default content"""
        self.driver.switch_to.default_content()
        logger.debug("Switched to default content")

    def switch_to_window(self, window_handle: str) -> None:
        """
        Switches to window

        Args:
            window_handle: Window handle
        """
        self.driver.switch_to.window(window_handle)
        logger.debug(f"Switched to window: {window_handle}")

    def get_window_handles(self) -> list[str]:
        """Gets list of window handles"""
        handles = self.driver.window_handles
        logger.debug(f"Found windows: {len(handles)}")
        return handles

    def close_current_window(self) -> None:
        """Closes current window"""
        self.driver.close()
        logger.debug("Current window closed")

    def maximize_window(self) -> None:
        """Maximizes window"""
        self.driver.maximize_window()
        logger.debug("Window maximized")

    def set_window_size(self, width: int, height: int) -> None:
        """
        Sets window size

        Args:
            width: Width
            height: Height
        """
        self.driver.set_window_size(width, height)
        logger.debug(f"Window size set: {width}x{height}")

    def get_window_size(self) -> dict:
        """Gets window size"""
        size = self.driver.get_window_size()
        logger.debug(f"Window size: {size}")
        return size
