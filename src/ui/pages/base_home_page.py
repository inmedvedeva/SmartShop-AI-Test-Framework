"""
Base class for home pages with common functionality
"""

from abc import ABC, abstractmethod

from loguru import logger

from src.ui.pages.base_page import BasePage


class BaseHomePage(BasePage, ABC):
    """Base class for home pages with common functionality"""

    def __init__(self, driver, base_url: str):
        super().__init__(driver)
        self.base_url = base_url

    def open_home_page(self) -> None:
        """Open the home page"""
        logger.info(f"Opening home page: {self.base_url}")
        self.driver.get(self.base_url)
        self.wait_for_page_load()

    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title

    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url

    @abstractmethod
    def get_expected_title(self) -> str:
        """Get expected page title - to be implemented by subclasses"""
        pass

    @abstractmethod
    def get_expected_url(self) -> str:
        """Get expected page URL - to be implemented by subclasses"""
        pass

    def verify_home_page_load(self) -> bool:
        """Verify that home page loaded correctly"""
        title = self.get_page_title()
        url = self.get_current_url()

        expected_title = self.get_expected_title()
        expected_url = self.get_expected_url()

        title_ok = expected_title in title
        url_ok = expected_url in url

        logger.info(f"Home page verification - Title: {title_ok}, URL: {url_ok}")

        return title_ok and url_ok
