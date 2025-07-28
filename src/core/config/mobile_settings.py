"""
Mobile testing configuration for Playwright
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class MobileDevice(Enum):
    """Supported mobile devices for testing"""

    IPHONE_12 = "iPhone 12"
    IPHONE_12_PRO = "iPhone 12 Pro"
    IPHONE_12_PRO_MAX = "iPhone 12 Pro Max"
    IPHONE_13 = "iPhone 13"
    IPHONE_13_PRO = "iPhone 13 Pro"
    IPHONE_13_PRO_MAX = "iPhone 13 Pro Max"
    IPHONE_14 = "iPhone 14"
    IPHONE_14_PLUS = "iPhone 14 Plus"
    IPHONE_14_PRO = "iPhone 14 Pro"
    IPHONE_14_PRO_MAX = "iPhone 14 Pro Max"
    IPHONE_15 = "iPhone 15"
    IPHONE_15_PLUS = "iPhone 15 Plus"
    IPHONE_15_PRO = "iPhone 15 Pro"
    IPHONE_15_PRO_MAX = "iPhone 15 Pro Max"
    IPHONE_SE = "iPhone SE"
    IPAD_AIR = "iPad Air"
    IPAD_PRO_11 = "iPad Pro 11"
    IPAD_PRO_12_9 = "iPad Pro 12.9"
    GALAXY_S20 = "Galaxy S20"
    GALAXY_S21 = "Galaxy S21"
    GALAXY_S22 = "Galaxy S22"
    GALAXY_S23 = "Galaxy S23"
    GALAXY_S24 = "Galaxy S24"
    GALAXY_TAB_S7 = "Galaxy Tab S7"
    GALAXY_TAB_S8 = "Galaxy Tab S8"
    GALAXY_TAB_S9 = "Galaxy Tab S9"
    PIXEL_5 = "Pixel 5"
    PIXEL_6 = "Pixel 6"
    PIXEL_7 = "Pixel 7"
    PIXEL_8 = "Pixel 8"
    PIXEL_TABLET = "Pixel Tablet"


@dataclass
class MobileConfig:
    """Mobile testing configuration"""

    device: MobileDevice
    browser: str = "chromium"  # chromium, firefox, webkit
    headless: bool = True
    slow_mo: int = 100  # milliseconds
    timeout: int = 30000  # milliseconds
    viewport: dict[str, int] = None
    user_agent: str = None
    locale: str = "en-US"
    timezone_id: str = "America/New_York"
    geolocation: dict[str, float] = None
    permissions: list[str] = None
    extra_http_headers: dict[str, str] = None
    ignore_https_errors: bool = False
    java_script_enabled: bool = True
    bypass_csp: bool = False
    color_scheme: str = "light"  # light, dark, no-preference
    reduced_motion: str = "no-preference"  # reduce, no-preference
    forced_colors: str = "no-preference"  # active, none


class MobileTestConfig:
    """Mobile testing configuration manager"""

    # Default mobile configurations
    DEFAULT_CONFIGS = {
        MobileDevice.IPHONE_12: MobileConfig(
            device=MobileDevice.IPHONE_12,
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        ),
        MobileDevice.IPHONE_14_PRO: MobileConfig(
            device=MobileDevice.IPHONE_14_PRO,
            viewport={"width": 393, "height": 852},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        ),
        MobileDevice.GALAXY_S23: MobileConfig(
            device=MobileDevice.GALAXY_S23,
            viewport={"width": 412, "height": 915},
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        ),
        MobileDevice.PIXEL_7: MobileConfig(
            device=MobileDevice.PIXEL_7,
            viewport={"width": 412, "height": 915},
            user_agent="Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        ),
        MobileDevice.IPAD_AIR: MobileConfig(
            device=MobileDevice.IPAD_AIR,
            viewport={"width": 820, "height": 1180},
            user_agent="Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        ),
        MobileDevice.GALAXY_TAB_S9: MobileConfig(
            device=MobileDevice.GALAXY_TAB_S9,
            viewport={"width": 1024, "height": 1368},
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-X710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        ),
    }

    @classmethod
    def get_config(cls, device: MobileDevice) -> MobileConfig:
        """Get configuration for specific device"""
        return cls.DEFAULT_CONFIGS.get(device, MobileConfig(device=device))

    @classmethod
    def get_all_devices(cls) -> list[MobileDevice]:
        """Get list of all supported devices"""
        return list(MobileDevice)

    @classmethod
    def get_ios_devices(cls) -> list[MobileDevice]:
        """Get list of iOS devices"""
        return [
            device
            for device in MobileDevice
            if device.value.startswith(("iPhone", "iPad"))
        ]

    @classmethod
    def get_android_devices(cls) -> list[MobileDevice]:
        """Get list of Android devices"""
        return [
            device
            for device in MobileDevice
            if device.value.startswith(("Galaxy", "Pixel"))
        ]

    @classmethod
    def get_phone_devices(cls) -> list[MobileDevice]:
        """Get list of phone devices (excluding tablets)"""
        return [
            device
            for device in MobileDevice
            if not device.value.startswith(("iPad", "Galaxy Tab", "Pixel Tablet"))
        ]

    @classmethod
    def get_tablet_devices(cls) -> list[MobileDevice]:
        """Get list of tablet devices"""
        return [
            device
            for device in MobileDevice
            if device.value.startswith(("iPad", "Galaxy Tab", "Pixel Tablet"))
        ]


# Common mobile test scenarios
MOBILE_TEST_SCENARIOS = {
    "responsive_design": "Test responsive design on different screen sizes",
    "touch_interactions": "Test touch gestures and interactions",
    "mobile_navigation": "Test mobile navigation menu and hamburger menu",
    "mobile_forms": "Test form interactions on mobile devices",
    "mobile_performance": "Test page load performance on mobile devices",
    "mobile_accessibility": "Test accessibility features on mobile",
    "mobile_seo": "Test mobile SEO elements and meta tags",
    "mobile_pwa": "Test Progressive Web App features",
    "mobile_notifications": "Test push notifications (if applicable)",
    "mobile_offline": "Test offline functionality",
    "mobile_orientation": "Test landscape and portrait orientations",
    "mobile_gestures": "Test swipe, pinch, and other mobile gestures",
}
