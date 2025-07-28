"""
Report management utilities for SmartShop AI Test Framework
"""

import json
import os
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.core.constants import REPORT_DIR, SCREENSHOT_DIR


class ReportManager:
    """Report management class"""

    def __init__(self, report_dir=REPORT_DIR):
        self.report_dir = Path(report_dir)
        self.screenshot_dir = Path(SCREENSHOT_DIR)
        self.allure_dir = self.report_dir / "allure-results"
        self.html_dir = self.report_dir / "html"

        # Create directories
        self.report_dir.mkdir(exist_ok=True)
        self.screenshot_dir.mkdir(exist_ok=True)
        self.allure_dir.mkdir(exist_ok=True)
        self.html_dir.mkdir(exist_ok=True)

    def save_screenshot(self, driver, name=None):
        """Save screenshot on test failure"""
        try:
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = f"screenshot_{timestamp}.png"

            screenshot_path = self.screenshot_dir / name
            driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)

        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return None

    def create_test_summary(self, test_results):
        """Create test summary report"""
        try:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(test_results),
                "passed": sum(1 for r in test_results if r.get("status") == "passed"),
                "failed": sum(1 for r in test_results if r.get("status") == "failed"),
                "skipped": sum(1 for r in test_results if r.get("status") == "skipped"),
                "results": test_results,
            }

            summary_path = self.report_dir / "test_summary.json"
            with open(summary_path, "w") as f:
                json.dump(summary, f, indent=2)

            logger.info(f"Test summary created: {summary_path}")
            return summary

        except Exception as e:
            logger.error(f"Failed to create test summary: {e}")
            return None

    def create_execution_report(self, execution_data):
        """Create execution report for Allure"""
        try:
            executor_data = {
                "name": "SmartShop AI Test Framework",
                "type": "github",
                "url": "https://github.com/your-username/SmartShop-AI-Test-Framework",
                "buildName": f"build-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "buildUrl": os.getenv("GITHUB_RUN_ID", ""),
                "executor": {"name": "GitHub Actions", "type": "github"},
            }

            executor_path = self.allure_dir / "executor.json"
            with open(executor_path, "w") as f:
                json.dump(executor_data, f, indent=2)

            logger.info(f"Execution report created: {executor_path}")
            return executor_data

        except Exception as e:
            logger.error(f"Failed to create execution report: {e}")
            return None

    def cleanup_old_reports(self, days=30):
        """Clean up old reports"""
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)

            for file_path in self.report_dir.rglob("*"):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_date:
                    file_path.unlink()
                    logger.info(f"Cleaned up old report: {file_path}")

            logger.info(f"Cleanup completed for reports older than {days} days")

        except Exception as e:
            logger.error(f"Failed to cleanup old reports: {e}")


def get_report_manager():
    """Factory function to get report manager"""
    return ReportManager()
