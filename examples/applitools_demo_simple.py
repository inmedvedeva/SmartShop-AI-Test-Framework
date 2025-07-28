#!/usr/bin/env python3
"""
Simple Applitools demo without API key
Shows how visual testing works with fallback to basic comparison
"""

import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.utils.visual_testing import VisualTester


def demo_visual_testing_without_applitools():
    """Demo visual testing without Applitools API key"""

    print("🤖 Visual Testing Demo (without Applitools API key)")
    print("=" * 60)
    print("This demo shows how visual testing works with basic image comparison")
    print("when Applitools API key is not configured.")
    print()

    # Setup WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    try:
        # Initialize visual tester
        visual_tester = VisualTester()

        print("📊 Visual Tester Status:")
        print(f"   Applitools Available: {'✅ Yes' if visual_tester.eyes else '❌ No'}")
        print(
            f"   Fallback Mode: {'✅ Active' if not visual_tester.eyes else '❌ Not needed'}"
        )
        print()

        # Demo 1: Basic visual check
        print("🎯 Demo 1: Basic Visual Check")
        print("-" * 40)

        driver.get("https://automationexercise.com/")
        time.sleep(3)

        result = visual_tester.check_page_layout("demo_home_page", driver)
        print(f"   Result: {result['status']}")

        if result["status"] == "baseline_created":
            print("   📁 New baseline created (first run)")
        elif result["status"] == "passed":
            print("   ✅ No visual differences detected")
        elif result["status"] == "failed":
            print("   ❌ Visual differences detected")
            if "diff_image" in result:
                print(f"   📷 Diff image: {result['diff_image']}")

        # Demo 2: Simulate changes
        print("\n🎨 Demo 2: Simulate Page Changes")
        print("-" * 40)

        # Make some changes to the page
        driver.execute_script(
            """
            document.body.style.backgroundColor = '#f0f0f0';
            document.querySelector('.header-middle').style.border = '3px solid red';
        """
        )
        time.sleep(2)

        result = visual_tester.check_page_layout("demo_changed_page", driver)
        print(f"   Result: {result['status']}")

        if result["status"] == "failed":
            print("   ❌ Changes detected (as expected)")
            if "differences" in result:
                diff_info = result["differences"]
                print(
                    f"   📈 Differences: {diff_info.get('total_differences', 0)} areas"
                )
        else:
            print("   ✅ No changes detected")

        # Demo 3: Region-specific check
        print("\n🎯 Demo 3: Region-Specific Check")
        print("-" * 40)

        # Find header element
        try:
            header = driver.find_element(By.CSS_SELECTOR, ".header-middle")
            header_location = header.location
            header_size = header.size

            region = (
                header_location["x"],
                header_location["y"],
                header_size["width"],
                header_size["height"],
            )

            print(f"   Checking header region: {region[2]}x{region[3]} pixels")

            result = visual_tester.check_page_layout(
                "demo_header_region", driver, region=region
            )
            print(f"   Result: {result['status']}")

        except Exception as e:
            print(f"   ❌ Error finding header: {e}")

        # Demo 4: Responsive testing
        print("\n📱 Demo 4: Responsive Testing")
        print("-" * 40)

        screen_sizes = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile"),
        ]

        for width, height, device in screen_sizes:
            driver.set_window_size(width, height)
            driver.refresh()
            time.sleep(3)

            result = visual_tester.check_page_layout(f"demo_{device.lower()}", driver)
            print(f"   {device}: {result['status']}")

        print("\n📋 Demo Summary:")
        print("   ✅ Basic visual testing works without Applitools")
        print("   ✅ Screenshot comparison is functional")
        print("   ✅ Region-specific testing available")
        print("   ✅ Responsive testing supported")
        print("   ⚠️  Limited AI analysis (no Applitools)")
        print("   ⚠️  Basic pixel comparison only")

        print("\n💡 To enable full AI-powered visual testing:")
        print("   1. Get API key from https://applitools.com/")
        print("   2. Run: python scripts/setup_applitools.py")
        print("   3. Enjoy AI-powered visual regression detection!")

    except Exception as e:
        print(f"❌ Demo error: {e}")

    finally:
        driver.quit()


def show_comparison():
    """Show comparison between basic and AI-powered visual testing"""

    print("\n🔄 Visual Testing Comparison")
    print("=" * 60)

    print("📊 Basic Visual Testing (Current Demo):")
    print("   ✅ Screenshot capture")
    print("   ✅ Pixel-by-pixel comparison")
    print("   ✅ Region-specific testing")
    print("   ✅ Responsive testing")
    print("   ❌ No AI analysis")
    print("   ❌ No smart change detection")
    print("   ❌ No baseline management")
    print("   ❌ Limited reporting")

    print("\n🤖 AI-Powered Visual Testing (with Applitools):")
    print("   ✅ All basic features")
    print("   ✅ AI-powered image analysis")
    print("   ✅ Smart change detection")
    print("   ✅ Automatic baseline management")
    print("   ✅ Ignore minor changes (time, animations)")
    print("   ✅ Focus on critical UI changes")
    print("   ✅ Detailed AI reports")
    print("   ✅ Cross-browser testing")
    print("   ✅ CI/CD integration")

    print("\n🎯 When to use each:")
    print("   Basic: Simple projects, learning, prototyping")
    print("   AI-Powered: Production apps, complex UI, CI/CD")


def main():
    """Main demo function"""

    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        show_comparison()
        return

    print("Welcome to Visual Testing Demo!")
    print("This demo shows visual testing capabilities without requiring an API key.")

    demo_visual_testing_without_applitools()

    print("\nFor comparison, run: python examples/applitools_demo_simple.py --compare")


if __name__ == "__main__":
    import sys

    main()
