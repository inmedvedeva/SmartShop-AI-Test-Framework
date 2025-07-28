#!/usr/bin/env python3
"""
Detailed example of Applitools Eyes usage
Demonstrates how AI-powered visual testing works
"""

import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.config.settings import settings
from src.core.utils.visual_testing import VisualTester


class ApplitoolsExample:
    """Example of Applitools Eyes usage for visual testing"""

    def __init__(self):
        self.driver = None
        self.visual_tester = VisualTester()
        self.setup_driver()

    def setup_driver(self):
        """Setup WebDriver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in background mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")  # Fixed window size

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def demonstrate_applitools_basic_usage(self):
        """
        Demonstration of basic Applitools Eyes usage

        How it works:
        1. Applitools takes a screenshot of the page
        2. Compares with baseline (reference image)
        3. Uses AI to analyze differences
        4. Ignores minor changes (animations, time)
        5. Focuses on critical UI changes
        """
        print("🔍 Demonstration of basic Applitools Eyes usage")
        print("=" * 60)

        try:
            # Open test page
            self.driver.get("https://automationexercise.com/")
            time.sleep(3)  # Wait for loading

            print("📸 Taking first screenshot (creating baseline)")

            # First run - creates baseline
            result = self.visual_tester.check_page_layout(
                "home_page_baseline", self.driver
            )

            print(f"✅ Result: {result['status']}")
            if result["status"] == "baseline_created":
                print("📁 New baseline created for comparison")

            # Simulate changes on the page (e.g., CSS changes)
            self.driver.execute_script(
                """
                document.body.style.backgroundColor = '#f0f0f0';
                document.querySelector('.header-middle').style.border = '2px solid red';
            """
            )

            print("\n🎨 Simulating changes on the page")
            print("   - Changed background color")
            print("   - Added red border to header")

            time.sleep(2)

            # Second run - compare with baseline
            print("\n🔍 Comparing with baseline")
            result = self.visual_tester.check_page_layout(
                "home_page_changed", self.driver
            )

            print(f"📊 Comparison result:")
            print(f"   Status: {result['status']}")

            if result["status"] == "failed":
                print("❌ Visual differences detected!")
                if "diff_image" in result:
                    print(f"   📷 Diff image saved: {result['diff_image']}")

                # Show difference details
                if "differences" in result:
                    diff_info = result["differences"]
                    print(f"   📈 Difference statistics:")
                    print(
                        f"      - Total differences: {diff_info.get('total_differences', 0)}"
                    )
                    print(
                        f"      - Difference size: {diff_info.get('difference_percentage', 0):.2f}%"
                    )

            elif result["status"] == "passed":
                print("✅ No visual differences detected")

        except Exception as e:
            print(f"❌ Error: {e}")

    def demonstrate_applitools_region_checking(self):
        """
        Demonstration of checking specific page regions

        Advantages:
        - Focus on important elements
        - Ignore dynamic content
        - More precise testing
        """
        print("\n🎯 Demonstration of checking specific regions")
        print("=" * 60)

        try:
            self.driver.get("https://automationexercise.com/")
            time.sleep(3)

            # Find header element
            header = self.driver.find_element(By.CSS_SELECTOR, ".header-middle")
            header_location = header.location
            header_size = header.size

            # Define region for checking (x, y, width, height)
            region = (
                header_location["x"],
                header_location["y"],
                header_size["width"],
                header_size["height"],
            )

            print(f"📍 Checking header region:")
            print(f"   Coordinates: x={region[0]}, y={region[1]}")
            print(f"   Size: {region[2]}x{region[3]} pixels")

            # Check only header region
            result = self.visual_tester.check_page_layout(
                "header_only", self.driver, region=region
            )

            print(f"📊 Header check result: {result['status']}")

            # Now check footer
            footer = self.driver.find_element(By.CSS_SELECTOR, ".footer-widget")
            footer_location = footer.location
            footer_size = footer.size

            footer_region = (
                footer_location["x"],
                footer_location["y"],
                footer_size["width"],
                footer_size["height"],
            )

            print(f"\n📍 Checking footer region:")
            print(f"   Coordinates: x={footer_region[0]}, y={footer_region[1]}")
            print(f"   Size: {footer_region[2]}x{footer_region[3]} pixels")

            result = self.visual_tester.check_page_layout(
                "footer_only", self.driver, region=footer_region
            )

            print(f"📊 Footer check result: {result['status']}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def demonstrate_applitools_responsive_testing(self):
        """
        Demonstration of testing on different screen sizes

        Applitools automatically:
        - Adapts to different resolutions
        - Considers responsive design
        - Compares elements in context of their size
        """
        print("\n📱 Demonstration of responsive testing")
        print("=" * 60)

        resolutions = [
            (1920, 1080, "Desktop"),
            (1366, 768, "Laptop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile"),
        ]

        for width, height, device_name in resolutions:
            print(f"\n📱 Testing on {device_name} ({width}x{height})")

            try:
                # Change window size
                self.driver.set_window_size(width, height)
                time.sleep(2)

                # Reload page to apply responsive styles
                self.driver.refresh()
                time.sleep(3)

                # Visual check
                result = self.visual_tester.check_page_layout(
                    f"home_page_{device_name.lower()}", self.driver
                )

                print(f"   📊 Result: {result['status']}")

                # Check that elements adapted
                try:
                    # Check for mobile menu on small screens
                    if width <= 768:
                        mobile_menu = self.driver.find_element(
                            By.CSS_SELECTOR, ".navbar-toggler"
                        )
                        print(f"   ✅ Mobile menu found")
                    else:
                        desktop_menu = self.driver.find_element(
                            By.CSS_SELECTOR, ".navbar-nav"
                        )
                        print(f"   ✅ Desktop menu displayed")
                except:
                    print(f"   ⚠️  Menu not found for {device_name}")

            except Exception as e:
                print(f"   ❌ Error for {device_name}: {e}")

    def demonstrate_applitools_ai_features(self):
        """
        Demonstration of Applitools AI capabilities

        AI functions:
        - Ignore minor changes
        - Detect critical UI issues
        - Analyze change context
        - Suggest fixes
        """
        print("\n🤖 Demonstration of Applitools AI capabilities")
        print("=" * 60)

        try:
            self.driver.get("https://automationexercise.com/")
            time.sleep(3)

            print("🧠 AI page analysis:")
            print("   - Element structure analysis")
            print("   - Important area detection")
            print("   - Sensitivity configuration")

            # Create baseline
            result = self.visual_tester.check_page_layout("ai_baseline", self.driver)

            # Simulate different types of changes
            changes = [
                (
                    "Minor color change",
                    """
                    document.body.style.color = '#666666';
                """,
                ),
                (
                    "Critical change - hide element",
                    """
                    document.querySelector('.header-middle').style.display = 'none';
                """,
                ),
                (
                    "Font size change",
                    """
                    document.body.style.fontSize = '18px';
                """,
                ),
                (
                    "Add new element",
                    """
                    var newDiv = document.createElement('div');
                    newDiv.innerHTML = '<h1>New Element</h1>';
                    newDiv.style.backgroundColor = 'red';
                    newDiv.style.padding = '20px';
                    document.body.insertBefore(newDiv, document.body.firstChild);
                """,
                ),
            ]

            for change_name, change_script in changes:
                print(f"\n🔧 Testing: {change_name}")

                # Apply change
                self.driver.execute_script(change_script)
                time.sleep(2)

                # Check with AI
                result = self.visual_tester.check_page_layout(
                    f"ai_test_{change_name.replace(' ', '_')}", self.driver
                )

                print(f"   📊 AI result: {result['status']}")

                if result["status"] == "failed":
                    print("   ❌ AI detected critical change")
                else:
                    print("   ✅ AI determined change as minor")

                # Restore page to original state
                self.driver.refresh()
                time.sleep(3)

        except Exception as e:
            print(f"❌ Error: {e}")

    def demonstrate_applitools_integration_with_tests(self):
        """
        Demonstration of Applitools integration with regular tests

        Integration advantages:
        - Automatic visual testing
        - Screenshot saving on errors
        - Detailed reporting
        """
        print("\n🧪 Demonstration of integration with tests")
        print("=" * 60)

        try:
            # Simulate test scenario
            print("🚀 Starting test scenario: Home page verification")

            # Step 1: Open page
            self.driver.get("https://automationexercise.com/")
            time.sleep(3)

            # Visual check after loading
            visual_result = self.visual_tester.check_page_layout(
                "test_step_1_loaded", self.driver
            )
            print(f"   ✅ Step 1: Page loaded - {visual_result['status']}")

            # Step 2: Check elements
            try:
                logo = self.driver.find_element(By.CSS_SELECTOR, ".logo a")
                assert logo.is_displayed(), "Logo not displayed"
                print("   ✅ Step 2: Logo found and displayed")
            except Exception as e:
                print(f"   ❌ Step 2: Logo error - {e}")

            # Visual check after interaction
            visual_result = self.visual_tester.check_page_layout(
                "test_step_2_logo_checked", self.driver
            )
            print(f"   📊 Visual check: {visual_result['status']}")

            # Step 3: Navigation
            try:
                products_link = self.driver.find_element(
                    By.CSS_SELECTOR, "a[href='/products']"
                )
                products_link.click()
                time.sleep(3)
                print("   ✅ Step 3: Navigated to products page")
            except Exception as e:
                print(f"   ❌ Step 3: Navigation error - {e}")

            # Visual check of new page
            visual_result = self.visual_tester.check_page_layout(
                "test_step_3_products_page", self.driver
            )
            print(f"   📊 Products visual check: {visual_result['status']}")

            print("\n📋 Final report:")
            print("   - All steps completed successfully")
            print("   - Visual checks performed")
            print("   - Screenshots saved for analysis")

        except Exception as e:
            print(f"❌ Error in test scenario: {e}")

    def show_applitools_configuration(self):
        """Shows Applitools configuration"""
        print("\n⚙️ Applitools Eyes Configuration")
        print("=" * 60)

        print("📁 Directory structure:")
        print(f"   Screenshots: {self.visual_tester.screenshot_dir}")
        print(f"   Baseline: {self.visual_tester.baseline_dir}")
        print(f"   Current: {self.visual_tester.current_dir}")
        print(f"   Diff: {self.visual_tester.diff_dir}")

        print("\n🔑 Settings:")
        print(
            f"   Applitools API Key: {'✅ Configured' if settings.applitools_api_key else '❌ Not configured'}"
        )
        print(f"   App Name: {settings.applitools_app_name}")
        print(
            f"   Applitools Available: {'✅ Yes' if self.visual_tester.eyes else '❌ No'}"
        )

        print("\n📊 Capabilities:")
        print("   ✅ AI-powered image analysis")
        print("   ✅ Automatic ignoring of minor changes")
        print("   ✅ Specific area checking")
        print("   ✅ Responsive testing")
        print("   ✅ Detailed reporting")
        print("   ✅ CI/CD integration")

    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()


def main():
    """Main demonstration function"""
    print("🤖 Applitools Eyes - Detailed Demonstration")
    print("=" * 80)
    print("This example shows how AI-powered visual testing works")
    print("using Applitools Eyes in our framework.")
    print()

    example = ApplitoolsExample()

    try:
        # Show configuration
        example.show_applitools_configuration()

        # Demonstrate capabilities
        example.demonstrate_applitools_basic_usage()
        example.demonstrate_applitools_region_checking()
        example.demonstrate_applitools_responsive_testing()
        example.demonstrate_applitools_ai_features()
        example.demonstrate_applitools_integration_with_tests()

        print("\n🎉 Demonstration completed!")
        print("📚 To get Applitools API key visit: https://applitools.com/")

    except Exception as e:
        print(f"❌ Error in demonstration: {e}")

    finally:
        example.cleanup()


if __name__ == "__main__":
    main()
