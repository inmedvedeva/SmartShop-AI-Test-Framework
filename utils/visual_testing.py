"""
AI-powered visual testing
Integration with Applitools and custom computer vision algorithms
"""

import os
import time
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from loguru import logger
from PIL import Image, ImageChops, ImageEnhance
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings

try:
    from applitools.selenium import Eyes, Target

    APPLITOOLS_AVAILABLE = True
except ImportError:
    APPLITOOLS_AVAILABLE = False
    logger.warning("Applitools not installed")


class VisualTester:
    """Class for AI-powered visual testing"""

    def __init__(self):
        self.eyes = None
        self.screenshot_dir = settings.screenshot_dir
        self.baseline_dir = os.path.join(self.screenshot_dir, "baseline")
        self.current_dir = os.path.join(self.screenshot_dir, "current")
        self.diff_dir = os.path.join(self.screenshot_dir, "diff")

        # Create directories if they don't exist
        for directory in [
            self.screenshot_dir,
            self.baseline_dir,
            self.current_dir,
            self.diff_dir,
        ]:
            os.makedirs(directory, exist_ok=True)

        # Initialize Applitools if available
        if APPLITOOLS_AVAILABLE and settings.applitools_api_key:
            self._init_applitools()

    def _init_applitools(self):
        """Initialize Applitools"""
        try:
            self.eyes = Eyes()
            self.eyes.api_key = settings.applitools_api_key
            self.eyes.app_name = settings.applitools_app_name
            logger.info("Applitools Eyes initialized")
        except Exception as e:
            logger.error(f"Error initializing Applitools: {e}")
            self.eyes = None

    def check_page_layout(
        self,
        page_name: str,
        driver: WebDriver,
        region: tuple[int, int, int, int] | None = None,
    ) -> dict[str, Any]:
        """
        Check page layout using AI

        Args:
            page_name: Page name
            driver: WebDriver
            region: Region to check (x, y, width, height)

        Returns:
            Dict with check results
        """
        logger.info(f"Starting visual check for page: {page_name}")

        # Take screenshot
        screenshot_path = self._take_screenshot(driver, page_name, region)

        # Check with Applitools if available
        if self.eyes:
            applitools_result = self._check_with_applitools(page_name, driver, region)
        else:
            applitools_result = {
                "status": "skipped",
                "reason": "Applitools not available",
            }

        # Check with custom algorithm
        custom_result = self._check_with_custom_algorithm(page_name, screenshot_path)

        # Analyze results
        overall_result = self._analyze_results(applitools_result, custom_result)

        logger.info(f"Visual check completed: {overall_result['status']}")
        return overall_result

    def _take_screenshot(
        self,
        driver: WebDriver,
        page_name: str,
        region: tuple[int, int, int, int] | None = None,
    ) -> str:
        """Take page screenshot"""
        timestamp = int(time.time())
        filename = f"{page_name}_{timestamp}.png"
        screenshot_path = os.path.join(self.current_dir, filename)

        # Take screenshot
        driver.save_screenshot(screenshot_path)

        # Crop region if specified
        if region:
            self._crop_screenshot(screenshot_path, region)

        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def _crop_screenshot(self, screenshot_path: str, region: tuple[int, int, int, int]):
        """Crop screenshot by specified region"""
        try:
            image = Image.open(screenshot_path)
            cropped = image.crop(region)
            cropped.save(screenshot_path)
            logger.info(f"Screenshot cropped by region: {region}")
        except Exception as e:
            logger.error(f"Error cropping screenshot: {e}")

    def _check_with_applitools(
        self,
        page_name: str,
        driver: WebDriver,
        region: tuple[int, int, int, int] | None,
    ) -> dict[str, Any]:
        """Check with Applitools"""
        try:
            self.eyes.open(driver, "SmartShop", page_name)

            if region:
                target = Target.region(region)
            else:
                target = Target.window()

            result = self.eyes.check(page_name, target)
            self.eyes.close()

            return {
                "status": "passed" if result else "failed",
                "applitools_result": result,
                "differences": result.differences if result else [],
            }

        except Exception as e:
            logger.error(f"Error checking with Applitools: {e}")
            return {"status": "error", "error": str(e)}

    def _check_with_custom_algorithm(
        self, page_name: str, screenshot_path: str
    ) -> dict[str, Any]:
        """Check with custom computer vision algorithm"""
        try:
            baseline_path = os.path.join(self.baseline_dir, f"{page_name}.png")

            # If no baseline, create it
            if not os.path.exists(baseline_path):
                self._create_baseline(screenshot_path, baseline_path)
                return {"status": "baseline_created", "message": "New baseline created"}

            # Compare with baseline
            differences = self._compare_images(baseline_path, screenshot_path)

            if differences["total_differences"] == 0:
                return {"status": "passed", "differences": differences}
            else:
                # Save diff image
                diff_path = os.path.join(
                    self.diff_dir, f"{page_name}_diff_{int(time.time())}.png"
                )
                self._save_diff_image(baseline_path, screenshot_path, diff_path)

                return {
                    "status": "failed",
                    "differences": differences,
                    "diff_image": diff_path,
                }

        except Exception as e:
            logger.error(f"Error in custom check: {e}")
            return {"status": "error", "error": str(e)}

    def _create_baseline(self, current_path: str, baseline_path: str):
        """Create baseline from current screenshot"""
        try:
            import shutil

            shutil.copy2(current_path, baseline_path)
            logger.info(f"Baseline created: {baseline_path}")
        except Exception as e:
            logger.error(f"Error creating baseline: {e}")

    def _compare_images(self, baseline_path: str, current_path: str) -> dict[str, Any]:
        """Compare two images and return differences"""
        try:
            # Load images
            baseline = cv2.imread(baseline_path)
            current = cv2.imread(current_path)

            if baseline is None or current is None:
                return {"status": "error", "error": "Failed to load images"}

            # Resize to same size
            if baseline.shape != current.shape:
                current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))

            # Calculate difference
            diff = cv2.absdiff(baseline, current)

            # Convert to grayscale for analysis
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            # Find differences
            _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            # Calculate statistics
            total_differences = len(contours)
            total_pixels = baseline.shape[0] * baseline.shape[1]
            difference_percentage = (
                (total_differences / total_pixels) * 100 if total_pixels > 0 else 0
            )

            return {
                "total_differences": total_differences,
                "difference_percentage": difference_percentage,
                "contours": contours,
            }

        except Exception as e:
            logger.error(f"Error comparing images: {e}")
            return {"status": "error", "error": str(e)}

    def _save_diff_image(self, baseline_path: str, current_path: str, diff_path: str):
        """Save difference image"""
        try:
            baseline = cv2.imread(baseline_path)
            current = cv2.imread(current_path)

            if baseline is None or current is None:
                return

            # Resize to same size
            if baseline.shape != current.shape:
                current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))

            # Calculate difference
            diff = cv2.absdiff(baseline, current)

            # Save diff image
            cv2.imwrite(diff_path, diff)
            logger.info(f"Diff image saved: {diff_path}")

        except Exception as e:
            logger.error(f"Error saving diff image: {e}")

    def _analyze_results(
        self, applitools_result: dict[str, Any], custom_result: dict[str, Any]
    ) -> dict[str, Any]:
        """Analyze results from both methods"""
        # Determine overall status
        if (
            applitools_result.get("status") == "passed"
            and custom_result.get("status") == "passed"
        ):
            overall_status = "passed"
        elif (
            applitools_result.get("status") == "failed"
            or custom_result.get("status") == "failed"
        ):
            overall_status = "failed"
        else:
            overall_status = "warning"

        # Generate recommendations
        recommendations = self._generate_recommendations(
            applitools_result, custom_result
        )

        return {
            "status": overall_status,
            "applitools": applitools_result,
            "custom": custom_result,
            "recommendations": recommendations,
            "timestamp": time.time(),
        }

    def _generate_recommendations(
        self, applitools_result: dict[str, Any], custom_result: dict[str, Any]
    ) -> list[str]:
        """Generate recommendations based on results"""
        recommendations = []

        if applitools_result.get("status") == "failed":
            recommendations.append(
                "Review Applitools differences and update baseline if needed"
            )

        if custom_result.get("status") == "failed":
            recommendations.append("Check for visual regressions in the UI")

        if applitools_result.get("status") == "skipped":
            recommendations.append(
                "Consider setting up Applitools for better visual testing"
            )

        return recommendations

    def check_element_visibility(
        self, driver: WebDriver, element_selector: str, timeout: int = 10
    ) -> dict[str, Any]:
        """
        Check element visibility using AI

        Args:
            driver: WebDriver
            element_selector: CSS selector or XPath
            timeout: Timeout in seconds

        Returns:
            Dict with visibility analysis
        """
        try:
            # Wait for element
            wait = WebDriverWait(driver, timeout)
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            )

            # Check if element is visible
            if not element.is_displayed():
                return {
                    "status": "failed",
                    "reason": "Element is not visible",
                    "visibility_score": 0.0,
                }

            # Take screenshot of element
            screenshot_data = element.screenshot_as_png

            # Analyze visibility
            visibility_analysis = self._analyze_element_visibility(screenshot_data)

            return {
                "status": "passed",
                "element_found": True,
                "is_visible": True,
                "visibility_score": visibility_analysis["visibility_score"],
                "analysis": visibility_analysis,
            }

        except Exception as e:
            logger.error(f"Error checking element visibility: {e}")
            return {
                "status": "error",
                "error": str(e),
                "element_found": False,
                "visibility_score": 0.0,
            }

    def _analyze_element_visibility(self, screenshot_data: bytes) -> dict[str, Any]:
        """Analyze element visibility from screenshot"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(screenshot_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                return {"visibility_score": 0.0, "error": "Failed to decode image"}

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Calculate brightness
            brightness = np.mean(gray)

            # Calculate contrast
            contrast = np.std(gray)

            # Detect text
            text_detected = self._detect_text(image)

            # Calculate visibility score
            visibility_score = self._calculate_visibility_score(
                brightness, contrast, text_detected
            )

            return {
                "visibility_score": visibility_score,
                "brightness": brightness,
                "contrast": contrast,
                "text_detected": text_detected,
                "image_size": image.shape,
            }

        except Exception as e:
            logger.error(f"Error analyzing element visibility: {e}")
            return {"visibility_score": 0.0, "error": str(e)}

    def _detect_text(self, image: np.ndarray) -> bool:
        """Detect if image contains text"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply threshold to find text-like regions
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Find contours
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            # Check if any contour looks like text (small, rectangular)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0

                # Text-like characteristics
                if 0.1 < aspect_ratio < 10 and 10 < w < 200 and 5 < h < 50:
                    return True

            return False

        except Exception as e:
            logger.error(f"Error detecting text: {e}")
            return False

    def _calculate_visibility_score(
        self, brightness: float, contrast: float, text_detected: bool
    ) -> float:
        """Calculate visibility score from metrics"""
        # Normalize brightness (0-255 to 0-1)
        brightness_score = min(brightness / 255.0, 1.0)

        # Normalize contrast (0-255 to 0-1)
        contrast_score = min(contrast / 255.0, 1.0)

        # Text bonus
        text_bonus = 0.2 if text_detected else 0.0

        # Calculate final score
        visibility_score = brightness_score * 0.4 + contrast_score * 0.4 + text_bonus

        return min(visibility_score, 1.0)
