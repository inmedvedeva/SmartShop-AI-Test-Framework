#!/usr/bin/env python3
"""
Mobile testing runner script for SmartShop AI Test Framework
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.config.mobile_settings import MobileDevice, MobileTestConfig


class MobileTestRunner:
    """Mobile test runner with device and browser management"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "reports"
        self.screenshots_dir = self.reports_dir / "screenshots"

        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)

    def install_playwright_browsers(self):
        """Install Playwright browsers"""
        logger.info("Installing Playwright browsers...")
        try:
            subprocess.run(
                [sys.executable, "-m", "playwright", "install"],
                check=True,
                cwd=self.project_root,
            )
            logger.info("✅ Playwright browsers installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install Playwright browsers: {e}")
            return False
        return True

    def run_tests_on_device(
        self,
        device: MobileDevice,
        browser: str = "chromium",
        test_pattern: str = None,
        markers: list[str] = None,
    ) -> bool:
        """Run tests on specific device and browser"""
        logger.info(f"Running tests on {device.value} with {browser}")

        # Build pytest command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-c",
            str(self.project_root / "pytest_mobile.ini"),
            "-v",
            "--tb=short",
        ]

        # Add test pattern if specified
        if test_pattern:
            cmd.append(f"tests/mobile/{test_pattern}")
        else:
            cmd.append("tests/mobile/")

        # Add markers if specified
        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])

        # Add device-specific marker (commented out to avoid filtering)
        # if device.value.startswith(("iPhone", "iPad")):
        #     cmd.extend(["-m", "ios"])
        # elif device.value.startswith(("Galaxy", "Pixel")):
        #     cmd.extend(["-m", "android"])
        #
        # if device.value.startswith(("iPad", "Galaxy Tab", "Pixel Tablet")):
        #     cmd.extend(["-m", "tablet"])
        # else:
        #     cmd.extend(["-m", "phone"])

        # Set environment variables for tests
        env = os.environ.copy()
        env["MOBILE_DEVICE"] = device.name
        env["MOBILE_BROWSER"] = browser

        # Run tests
        try:
            result = subprocess.run(
                cmd, cwd=self.project_root, capture_output=True, text=True, env=env
            )

            if result.returncode == 0:
                logger.info(f"✅ Tests passed on {device.value} with {browser}")
                return True
            else:
                logger.error(f"❌ Tests failed on {device.value} with {browser}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                return False

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to run tests on {device.value}: {e}")
            return False

    def run_cross_browser_tests(
        self, device: MobileDevice, test_pattern: str = None
    ) -> dict[str, bool]:
        """Run tests on all browsers for a device"""
        browsers = ["chromium", "firefox", "webkit"]
        results = {}

        logger.info(f"Running cross-browser tests on {device.value}")

        for browser in browsers:
            success = self.run_tests_on_device(device, browser, test_pattern)
            results[browser] = success

        return results

    def run_cross_device_tests(
        self, test_pattern: str = None, browsers: list[str] = None
    ) -> dict[str, dict[str, bool]]:
        """Run tests on multiple devices"""
        if browsers is None:
            browsers = ["chromium"]  # Default to chromium for speed

        # Select representative devices
        devices = [
            MobileDevice.IPHONE_12,  # iOS phone
            MobileDevice.IPHONE_14_PRO,  # iOS phone (newer)
            MobileDevice.GALAXY_S23,  # Android phone
            MobileDevice.PIXEL_7,  # Android phone (Google)
            MobileDevice.IPAD_AIR,  # iOS tablet
            MobileDevice.GALAXY_TAB_S9,  # Android tablet
        ]

        results = {}

        for device in devices:
            device_results = {}
            for browser in browsers:
                success = self.run_tests_on_device(device, browser, test_pattern)
                device_results[browser] = success
            results[device.value] = device_results

        return results

    def run_specific_test_scenarios(self, scenarios: list[str]) -> dict[str, bool]:
        """Run specific test scenarios across devices"""
        scenario_markers = {
            "responsive": ["responsive"],
            "gestures": ["gestures"],
            "performance": ["performance"],
            "accessibility": ["accessibility"],
            "navigation": ["mobile"],
            "forms": ["mobile"],
            "search": ["mobile"],
        }

        results = {}

        for scenario in scenarios:
            if scenario in scenario_markers:
                markers = scenario_markers[scenario]
                logger.info(f"Running {scenario} tests")

                # Run on representative devices
                devices = [MobileDevice.IPHONE_12, MobileDevice.GALAXY_S23]
                scenario_results = []

                for device in devices:
                    success = self.run_tests_on_device(
                        device, "chromium", markers=markers
                    )
                    scenario_results.append(success)

                results[scenario] = all(scenario_results)
            else:
                logger.warning(f"Unknown scenario: {scenario}")
                results[scenario] = False

        return results

    def generate_report(self, results: dict[str, Any]):
        """Generate test execution report with timestamp"""
        from datetime import datetime

        # Create timestamped report directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.reports_dir / "mobile" / timestamp
        report_dir.mkdir(parents=True, exist_ok=True)

        # Generate report files
        summary_file = report_dir / "summary.md"
        json_file = report_dir / "results.json"

        # Write summary report
        with open(summary_file, "w") as f:
            f.write("# Mobile Test Execution Report\n\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Report ID: {timestamp}\n\n")

            f.write("## Test Results Summary\n\n")

            if "cross_device" in results:
                f.write("### Cross-Device Compatibility\n\n")
                f.write("| Device | Browser | Status |\n")
                f.write("|--------|---------|--------|\n")

                for device, device_results in results["cross_device"].items():
                    for browser, success in device_results.items():
                        status = "✅ PASS" if success else "❌ FAIL"
                        f.write(f"| {device} | {browser} | {status} |\n")

            if "scenarios" in results:
                f.write("\n### Test Scenarios\n\n")
                f.write("| Scenario | Status |\n")
                f.write("|----------|--------|\n")

                for scenario, success in results["scenarios"].items():
                    status = "✅ PASS" if success else "❌ FAIL"
                    f.write(f"| {scenario} | {status} |\n")

            f.write("\n## Device Coverage\n\n")
            f.write(f"- iOS Devices: {len(MobileTestConfig.get_ios_devices())}\n")
            f.write(
                f"- Android Devices: {len(MobileTestConfig.get_android_devices())}\n"
            )
            f.write(f"- Phones: {len(MobileTestConfig.get_phone_devices())}\n")
            f.write(f"- Tablets: {len(MobileTestConfig.get_tablet_devices())}\n")

        # Write JSON report for programmatic access
        import json

        with open(json_file, "w") as f:
            json.dump(
                {
                    "timestamp": timestamp,
                    "generated_at": datetime.now().isoformat(),
                    "results": results,
                    "device_coverage": {
                        "ios_devices": len(MobileTestConfig.get_ios_devices()),
                        "android_devices": len(MobileTestConfig.get_android_devices()),
                        "phones": len(MobileTestConfig.get_phone_devices()),
                        "tablets": len(MobileTestConfig.get_tablet_devices()),
                    },
                },
                f,
                indent=2,
            )

        # Create latest symlink (for easy access)
        latest_link = self.reports_dir / "mobile" / "latest"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(timestamp)

        logger.info(f"Reports generated in: {report_dir}")
        logger.info(f"Summary: {summary_file}")
        logger.info(f"JSON: {json_file}")
        logger.info(f"Latest: {latest_link}")

        return report_dir


def main():
    """Main function for mobile test runner"""
    parser = argparse.ArgumentParser(
        description="Mobile Test Runner for SmartShop AI Test Framework"
    )

    parser.add_argument(
        "--install-browsers", action="store_true", help="Install Playwright browsers"
    )

    parser.add_argument(
        "--device",
        type=str,
        choices=[d.name for d in MobileDevice],
        help="Run tests on specific device",
    )

    parser.add_argument(
        "--browser",
        type=str,
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser engine to use",
    )

    parser.add_argument(
        "--cross-browser",
        action="store_true",
        help="Run tests on all browsers for specified device",
    )

    parser.add_argument(
        "--cross-device", action="store_true", help="Run tests on multiple devices"
    )

    parser.add_argument(
        "--scenarios",
        nargs="+",
        choices=[
            "responsive",
            "gestures",
            "performance",
            "accessibility",
            "navigation",
            "forms",
            "search",
        ],
        help="Run specific test scenarios",
    )

    parser.add_argument("--test-pattern", type=str, help="Test file pattern to run")

    parser.add_argument("--markers", nargs="+", help="Pytest markers to filter tests")

    args = parser.parse_args()

    # Setup logging
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add("logs/mobile_tests.log", rotation="1 day", retention="7 days")

    runner = MobileTestRunner()

    # Install browsers if requested
    if args.install_browsers:
        if not runner.install_playwright_browsers():
            sys.exit(1)

    results = {}

    # Run tests based on arguments
    if args.device:
        device = MobileDevice[args.device]

        if args.cross_browser:
            results["cross_browser"] = runner.run_cross_browser_tests(
                device, args.test_pattern
            )
        else:
            success = runner.run_tests_on_device(
                device, args.browser, args.test_pattern, args.markers
            )
            results["single_device"] = {device.value: {args.browser: success}}

    elif args.cross_device:
        browsers = ["chromium", "firefox"] if args.cross_browser else ["chromium"]
        results["cross_device"] = runner.run_cross_device_tests(
            args.test_pattern, browsers
        )

    elif args.scenarios:
        results["scenarios"] = runner.run_specific_test_scenarios(args.scenarios)

    else:
        # Default: run cross-device tests
        logger.info("Running default cross-device tests")
        results["cross_device"] = runner.run_cross_device_tests()

    # Generate report
    runner.generate_report(results)

    # Exit with appropriate code
    if any(
        not all(device_results.values())
        for device_results in results.get("cross_device", {}).values()
    ):
        logger.error("Some tests failed")
        sys.exit(1)
    else:
        logger.info("All tests passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
