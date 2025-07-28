"""
Visual testing utilities for SmartShop AI Test Framework
"""

from pathlib import Path
from typing import Any

import cv2
import numpy as np
from loguru import logger
from PIL import Image, ImageChops

from src.core.constants import SCREENSHOT_DIR


class VisualTester:
    """Visual testing utilities"""

    def __init__(
        self,
        baseline_dir: str = f"{SCREENSHOT_DIR}/baseline",
        current_dir: str = f"{SCREENSHOT_DIR}/current",
        diff_dir: str = f"{SCREENSHOT_DIR}/diff",
    ):
        self.baseline_dir = Path(baseline_dir)
        self.current_dir = Path(current_dir)
        self.diff_dir = Path(diff_dir)

        # Create directories
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.current_dir.mkdir(parents=True, exist_ok=True)
        self.diff_dir.mkdir(parents=True, exist_ok=True)

    def compare_images(
        self, baseline_path: str, current_path: str, threshold: float = 0.95
    ) -> dict[str, Any]:
        """Compare two images and return similarity score"""
        try:
            # Load images
            baseline_img = cv2.imread(baseline_path)
            current_img = cv2.imread(current_path)

            if baseline_img is None or current_img is None:
                logger.error("Failed to load images for comparison")
                return {
                    "similar": False,
                    "score": 0.0,
                    "error": "Failed to load images",
                }

            # Ensure same size
            if baseline_img.shape != current_img.shape:
                current_img = cv2.resize(
                    current_img, (baseline_img.shape[1], baseline_img.shape[0])
                )

            # Convert to grayscale for comparison
            baseline_gray = cv2.cvtColor(baseline_img, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)

            # Calculate similarity using template matching
            result = cv2.matchTemplate(
                current_gray, baseline_gray, cv2.TM_CCOEFF_NORMED
            )
            similarity_score = result[0][0]

            is_similar = similarity_score >= threshold

            result = {
                "similar": is_similar,
                "score": float(similarity_score),
                "threshold": threshold,
                "baseline_path": baseline_path,
                "current_path": current_path,
            }

            if not is_similar:
                # Create difference image
                diff_path = self._create_diff_image(
                    baseline_img, current_img, baseline_path
                )
                result["diff_path"] = diff_path

            logger.info(
                f"Image comparison: score={similarity_score:.3f}, "
                f"similar={is_similar}"
            )
            return result

        except Exception as e:
            logger.error(f"Error comparing images: {e}")
            return {"similar": False, "score": 0.0, "error": str(e)}

    def _create_diff_image(
        self, baseline_img: np.ndarray, current_img: np.ndarray, baseline_path: str
    ) -> str:
        """Create difference image"""
        try:
            # Convert to PIL images for difference calculation
            baseline_pil = Image.fromarray(
                cv2.cvtColor(baseline_img, cv2.COLOR_BGR2RGB)
            )
            current_pil = Image.fromarray(cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB))

            # Calculate difference
            diff = ImageChops.difference(baseline_pil, current_pil)

            # Convert back to OpenCV format
            diff_cv = cv2.cvtColor(np.array(diff), cv2.COLOR_RGB2BGR)

            # Save difference image
            baseline_name = Path(baseline_path).stem
            diff_path = self.diff_dir / f"{baseline_name}_diff.png"
            cv2.imwrite(str(diff_path), diff_cv)

            logger.info(f"Difference image saved: {diff_path}")
            return str(diff_path)

        except Exception as e:
            logger.error(f"Error creating diff image: {e}")
            return ""

    def find_image_in_screenshot(
        self, screenshot_path: str, template_path: str, threshold: float = 0.8
    ) -> tuple[int, int, int, int] | None:
        """Find template image within screenshot"""
        try:
            # Load images
            screenshot = cv2.imread(screenshot_path)
            template = cv2.imread(template_path)

            if screenshot is None or template is None:
                logger.error("Failed to load images for template matching")
                return None

            # Perform template matching
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                # Get template dimensions
                h, w = template.shape[:2]
                x, y = max_loc

                # Return bounding box (x, y, width, height)
                bbox = (x, y, w, h)
                logger.info(f"Template found at {bbox} with confidence {max_val:.3f}")
                return bbox
            else:
                logger.warning(
                    f"Template not found, best match confidence: {max_val:.3f}"
                )
                return None

        except Exception as e:
            logger.error(f"Error in template matching: {e}")
            return None

    def create_baseline(self, screenshot_path: str, baseline_name: str) -> bool:
        """Create baseline image from screenshot"""
        try:
            baseline_path = self.baseline_dir / f"{baseline_name}.png"

            # Copy screenshot to baseline
            import shutil

            shutil.copy2(screenshot_path, baseline_path)

            logger.info(f"Baseline created: {baseline_path}")
            return True

        except Exception as e:
            logger.error(f"Error creating baseline: {e}")
            return False

    def update_baseline(self, baseline_name: str, new_screenshot_path: str) -> bool:
        """Update existing baseline with new screenshot"""
        try:
            baseline_path = self.baseline_dir / f"{baseline_name}.png"

            if not baseline_path.exists():
                logger.warning(f"Baseline not found: {baseline_path}")
                return self.create_baseline(new_screenshot_path, baseline_name)

            # Backup old baseline
            backup_path = self.baseline_dir / f"{baseline_name}_backup.png"
            import shutil

            shutil.copy2(baseline_path, backup_path)

            # Update with new screenshot
            shutil.copy2(new_screenshot_path, baseline_path)

            logger.info(f"Baseline updated: {baseline_path}")
            return True

        except Exception as e:
            logger.error(f"Error updating baseline: {e}")
            return False

    def get_baseline_path(self, baseline_name: str) -> str | None:
        """Get path to baseline image"""
        baseline_path = self.baseline_dir / f"{baseline_name}.png"
        if baseline_path.exists():
            return str(baseline_path)
        else:
            logger.warning(f"Baseline not found: {baseline_path}")
            return None

    def list_baselines(self) -> list:
        """List all available baselines"""
        baselines = []
        for file_path in self.baseline_dir.glob("*.png"):
            baselines.append(file_path.stem)
        return baselines

    def cleanup_old_diffs(self, days: int = 7):
        """Clean up old difference images"""
        try:
            import time

            cutoff_time = time.time() - (days * 24 * 60 * 60)

            for file_path in self.diff_dir.glob("*_diff.png"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"Cleaned up old diff: {file_path}")

            logger.info(f"Cleanup completed for diffs older than {days} days")

        except Exception as e:
            logger.error(f"Error cleaning up old diffs: {e}")


class ApplitoolsVisualTester:
    """Applitools visual testing integration"""

    def __init__(self, api_key: str, app_name: str = "SmartShop AI Test Framework"):
        self.api_key = api_key
        self.app_name = app_name
        self.eyes = None
        self._initialize_eyes()

    def _initialize_eyes(self):
        """Initialize Applitools Eyes"""
        try:
            from applitools.selenium import Eyes

            self.eyes = Eyes()
            self.eyes.api_key = self.api_key
            logger.info("Applitools Eyes initialized")
        except ImportError:
            logger.warning("Applitools not available, install eyes-selenium package")
        except Exception as e:
            logger.error(f"Error initializing Applitools Eyes: {e}")

    def start_test(self, test_name: str, driver):
        """Start Applitools test"""
        if not self.eyes:
            logger.error("Applitools Eyes not initialized")
            return False

        try:
            self.eyes.open(driver, self.app_name, test_name)
            logger.info(f"Applitools test started: {test_name}")
            return True
        except Exception as e:
            logger.error(f"Error starting Applitools test: {e}")
            return False

    def check_window(self, tag: str = None):
        """Check current window"""
        if not self.eyes:
            logger.error("Applitools Eyes not initialized")
            return False

        try:
            self.eyes.check_window(tag)
            logger.info(f"Window check completed: {tag}")
            return True
        except Exception as e:
            logger.error(f"Error checking window: {e}")
            return False

    def check_element(self, element, tag: str = None):
        """Check specific element"""
        if not self.eyes:
            logger.error("Applitools Eyes not initialized")
            return False

        try:
            self.eyes.check_element(element, tag)
            logger.info(f"Element check completed: {tag}")
            return True
        except Exception as e:
            logger.error(f"Error checking element: {e}")
            return False

    def close_test(self):
        """Close Applitools test"""
        if not self.eyes:
            logger.error("Applitools Eyes not initialized")
            return False

        try:
            self.eyes.close()
            logger.info("Applitools test closed")
            return True
        except Exception as e:
            logger.error(f"Error closing Applitools test: {e}")
            return False

    def abort_test(self):
        """Abort Applitools test"""
        if not self.eyes:
            logger.error("Applitools Eyes not initialized")
            return False

        try:
            self.eyes.abort()
            logger.info("Applitools test aborted")
            return True
        except Exception as e:
            logger.error(f"Error aborting Applitools test: {e}")
            return False


def get_visual_tester() -> VisualTester:
    """Factory function to get visual tester"""
    return VisualTester()


def get_applitools_tester(
    api_key: str, app_name: str = "SmartShop AI Test Framework"
) -> ApplitoolsVisualTester:
    """Factory function to get Applitools tester"""
    return ApplitoolsVisualTester(api_key, app_name)
