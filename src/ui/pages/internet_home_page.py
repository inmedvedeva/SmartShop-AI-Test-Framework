"""
The Internet Home Page Object Model
Page Object for https://the-internet.herokuapp.com/
"""

from loguru import logger
from selenium.webdriver.common.by import By

from src.ui.pages.base_page import BasePage


class InternetHomePage(BasePage):
    """Page Object for The Internet Home Page"""

    # Locators
    HEADING = (By.CSS_SELECTOR, "h1.heading")
    SUBHEADING = (By.CSS_SELECTOR, "h2")

    # Navigation links
    AB_TESTING_LINK = (By.CSS_SELECTOR, "a[href='/abtest']")
    ADD_REMOVE_ELEMENTS_LINK = (By.CSS_SELECTOR, "a[href='/add_remove_elements/']")
    BASIC_AUTH_LINK = (By.CSS_SELECTOR, "a[href='/basic_auth']")
    BROKEN_IMAGES_LINK = (By.CSS_SELECTOR, "a[href='/broken_images']")
    CHECKBOXES_LINK = (By.CSS_SELECTOR, "a[href='/checkboxes']")
    CONTEXT_MENU_LINK = (By.CSS_SELECTOR, "a[href='/context_menu']")
    DIGEST_AUTH_LINK = (By.CSS_SELECTOR, "a[href='/digest_auth']")
    DISAPPEARING_ELEMENTS_LINK = (By.CSS_SELECTOR, "a[href='/disappearing_elements']")
    DRAG_AND_DROP_LINK = (By.CSS_SELECTOR, "a[href='/drag_and_drop']")
    DROPDOWN_LINK = (By.CSS_SELECTOR, "a[href='/dropdown']")
    DYNAMIC_CONTENT_LINK = (By.CSS_SELECTOR, "a[href='/dynamic_content']")
    DYNAMIC_CONTROLS_LINK = (By.CSS_SELECTOR, "a[href='/dynamic_controls']")
    DYNAMIC_LOADING_LINK = (By.CSS_SELECTOR, "a[href='/dynamic_loading']")
    ENTRY_AD_LINK = (By.CSS_SELECTOR, "a[href='/entry_ad']")
    EXIT_INTENT_LINK = (By.CSS_SELECTOR, "a[href='/exit_intent']")
    FILE_DOWNLOAD_LINK = (By.CSS_SELECTOR, "a[href='/download']")
    FILE_UPLOAD_LINK = (By.CSS_SELECTOR, "a[href='/upload']")
    FLOATING_MENU_LINK = (By.CSS_SELECTOR, "a[href='/floating_menu']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/forgot_password']")
    FORM_AUTHENTICATION_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    FRAMES_LINK = (By.CSS_SELECTOR, "a[href='/frames']")
    GEOLOCATION_LINK = (By.CSS_SELECTOR, "a[href='/geolocation']")
    HORIZONTAL_SLIDER_LINK = (By.CSS_SELECTOR, "a[href='/horizontal_slider']")
    HOVERS_LINK = (By.CSS_SELECTOR, "a[href='/hovers']")
    INFINITE_SCROLL_LINK = (By.CSS_SELECTOR, "a[href='/infinite_scroll']")
    INPUTS_LINK = (By.CSS_SELECTOR, "a[href='/inputs']")
    JQUERY_UI_MENUS_LINK = (By.CSS_SELECTOR, "a[href='/jqueryui/menu']")
    JAVASCRIPT_ALERTS_LINK = (By.CSS_SELECTOR, "a[href='/javascript_alerts']")
    JAVASCRIPT_ONLOAD_EVENT_ERROR_LINK = (
        By.CSS_SELECTOR,
        "a[href='/javascript_error']",
    )
    KEY_PRESSES_LINK = (By.CSS_SELECTOR, "a[href='/key_presses']")
    LARGE_AND_DEEP_DOM_LINK = (By.CSS_SELECTOR, "a[href='/large']")
    MULTIPLE_WINDOWS_LINK = (By.CSS_SELECTOR, "a[href='/windows']")
    NESTED_FRAMES_LINK = (By.CSS_SELECTOR, "a[href='/nested_frames']")
    NOTIFICATION_MESSAGES_LINK = (
        By.CSS_SELECTOR,
        "a[href='/notification_message_rendered']",
    )
    REDIRECT_LINK = (By.CSS_SELECTOR, "a[href='/redirector']")
    REQUEST_PASSWORD_RESET_LINK = (By.CSS_SELECTOR, "a[href='/forgot_password']")
    SORTABLE_DATA_TABLES_LINK = (By.CSS_SELECTOR, "a[href='/tables']")
    STATUS_CODES_LINK = (By.CSS_SELECTOR, "a[href='/status_codes']")
    TYPOS_LINK = (By.CSS_SELECTOR, "a[href='/typos']")
    WYSIWYG_EDITOR_LINK = (By.CSS_SELECTOR, "a[href='/tinymce']")

    # All links
    ALL_LINKS = (By.CSS_SELECTOR, "a[href]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://the-internet.herokuapp.com/"

    def open_home_page(self):
        """Open the home page"""
        logger.info(f"Opening The Internet home page: {self.url}")
        self.driver.get(self.url)
        self.wait_for_page_load()
        return self

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def get_heading(self):
        """Get main heading"""
        try:
            heading = self.find_element(self.HEADING)
            return heading.text
        except Exception:
            return None

    def get_subheading(self):
        """Get subheading"""
        try:
            subheading = self.find_element(self.SUBHEADING)
            return subheading.text
        except Exception:
            return None

    def click_link(self, link_name: str):
        """Click on a specific link by name"""
        logger.info(f"Clicking on link: {link_name}")

        link_map = {
            "ab testing": self.AB_TESTING_LINK,
            "add/remove elements": self.ADD_REMOVE_ELEMENTS_LINK,
            "basic auth": self.BASIC_AUTH_LINK,
            "broken images": self.BROKEN_IMAGES_LINK,
            "checkboxes": self.CHECKBOXES_LINK,
            "context menu": self.CONTEXT_MENU_LINK,
            "digest auth": self.DIGEST_AUTH_LINK,
            "disappearing elements": self.DISAPPEARING_ELEMENTS_LINK,
            "drag and drop": self.DRAG_AND_DROP_LINK,
            "dropdown": self.DROPDOWN_LINK,
            "dynamic content": self.DYNAMIC_CONTENT_LINK,
            "dynamic controls": self.DYNAMIC_CONTROLS_LINK,
            "dynamic loading": self.DYNAMIC_LOADING_LINK,
            "entry ad": self.ENTRY_AD_LINK,
            "exit intent": self.EXIT_INTENT_LINK,
            "file download": self.FILE_DOWNLOAD_LINK,
            "file upload": self.FILE_UPLOAD_LINK,
            "floating menu": self.FLOATING_MENU_LINK,
            "forgot password": self.FORGOT_PASSWORD_LINK,
            "form authentication": self.FORM_AUTHENTICATION_LINK,
            "frames": self.FRAMES_LINK,
            "geolocation": self.GEOLOCATION_LINK,
            "horizontal slider": self.HORIZONTAL_SLIDER_LINK,
            "hovers": self.HOVERS_LINK,
            "infinite scroll": self.INFINITE_SCROLL_LINK,
            "inputs": self.INPUTS_LINK,
            "jquery ui menus": self.JQUERY_UI_MENUS_LINK,
            "javascript alerts": self.JAVASCRIPT_ALERTS_LINK,
            "javascript onload event error": self.JAVASCRIPT_ONLOAD_EVENT_ERROR_LINK,
            "key presses": self.KEY_PRESSES_LINK,
            "large and deep dom": self.LARGE_AND_DEEP_DOM_LINK,
            "multiple windows": self.MULTIPLE_WINDOWS_LINK,
            "nested frames": self.NESTED_FRAMES_LINK,
            "notification messages": self.NOTIFICATION_MESSAGES_LINK,
            "redirect": self.REDIRECT_LINK,
            "request password reset": self.REQUEST_PASSWORD_RESET_LINK,
            "sortable data tables": self.SORTABLE_DATA_TABLES_LINK,
            "status codes": self.STATUS_CODES_LINK,
            "typos": self.TYPOS_LINK,
            "wysiwyg editor": self.WYSIWYG_EDITOR_LINK,
        }

        if link_name.lower() in link_map:
            self.click_element(link_map[link_name.lower()])
        else:
            logger.warning(f"Link '{link_name}' not found")

        return self

    def get_all_links(self):
        """Get all available links on the page"""
        logger.info("Getting all available links")
        links = self.find_elements(self.ALL_LINKS)
        link_list = []

        for link in links:
            try:
                link_list.append(
                    {
                        "text": link.text,
                        "href": link.get_attribute("href"),
                        "visible": link.is_displayed(),
                    }
                )
            except Exception as e:
                logger.warning(f"Could not extract link info: {e}")

        return link_list

    def get_links_count(self):
        """Get total number of links"""
        links = self.find_elements(self.ALL_LINKS)
        return len(links)

    def is_link_visible(self, link_name: str):
        """Check if a specific link is visible"""
        try:
            link_map = {
                "ab testing": self.AB_TESTING_LINK,
                "add/remove elements": self.ADD_REMOVE_ELEMENTS_LINK,
                "basic auth": self.BASIC_AUTH_LINK,
                "broken images": self.BROKEN_IMAGES_LINK,
                "checkboxes": self.CHECKBOXES_LINK,
                "context menu": self.CONTEXT_MENU_LINK,
                "digest auth": self.DIGEST_AUTH_LINK,
                "disappearing elements": self.DISAPPEARING_ELEMENTS_LINK,
                "drag and drop": self.DRAG_AND_DROP_LINK,
                "dropdown": self.DROPDOWN_LINK,
                "dynamic content": self.DYNAMIC_CONTENT_LINK,
                "dynamic controls": self.DYNAMIC_CONTROLS_LINK,
                "dynamic loading": self.DYNAMIC_LOADING_LINK,
                "entry ad": self.ENTRY_AD_LINK,
                "exit intent": self.EXIT_INTENT_LINK,
                "file download": self.FILE_DOWNLOAD_LINK,
                "file upload": self.FILE_UPLOAD_LINK,
                "floating menu": self.FLOATING_MENU_LINK,
                "forgot password": self.FORGOT_PASSWORD_LINK,
                "form authentication": self.FORM_AUTHENTICATION_LINK,
                "frames": self.FRAMES_LINK,
                "geolocation": self.GEOLOCATION_LINK,
                "horizontal slider": self.HORIZONTAL_SLIDER_LINK,
                "hovers": self.HOVERS_LINK,
                "infinite scroll": self.INFINITE_SCROLL_LINK,
                "inputs": self.INPUTS_LINK,
                "jquery ui menus": self.JQUERY_UI_MENUS_LINK,
                "javascript alerts": self.JAVASCRIPT_ALERTS_LINK,
                "javascript onload event error": self.JAVASCRIPT_ONLOAD_EVENT_ERROR_LINK,
                "key presses": self.KEY_PRESSES_LINK,
                "large and deep dom": self.LARGE_AND_DEEP_DOM_LINK,
                "multiple windows": self.MULTIPLE_WINDOWS_LINK,
                "nested frames": self.NESTED_FRAMES_LINK,
                "notification messages": self.NOTIFICATION_MESSAGES_LINK,
                "redirect": self.REDIRECT_LINK,
                "request password reset": self.REQUEST_PASSWORD_RESET_LINK,
                "sortable data tables": self.SORTABLE_DATA_TABLES_LINK,
                "status codes": self.STATUS_CODES_LINK,
                "typos": self.TYPOS_LINK,
                "wysiwyg editor": self.WYSIWYG_EDITOR_LINK,
            }

            if link_name.lower() in link_map:
                element = self.find_element(link_map[link_name.lower()])
                return element.is_displayed()
            else:
                return False
        except Exception:
            return False
