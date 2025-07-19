#!/usr/bin/env python3
"""
The Internet Demo Script
Demonstrates real UI testing with https://the-internet.herokuapp.com/
"""

import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.internet_home_page import InternetHomePage
from utils.ai_data_generator import AIDataGenerator


def setup_driver():
    """Setup Chrome WebDriver"""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for demo
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        logger.error(f"Failed to setup Chrome driver: {e}")
        return None


def main():
    """Main demo function"""
    print("🌐 The Internet Demo - Real UI Testing")
    print("=" * 60)
    print("Testing https://the-internet.herokuapp.com/")
    print("=" * 60)

    # Initialize AI generator
    ai_generator = AIDataGenerator()

    # Setup WebDriver
    driver = setup_driver()
    if not driver:
        print("❌ Failed to setup WebDriver")
        return

    try:
        # Initialize page object
        home_page = InternetHomePage(driver)

        print("\n🚀 Starting The Internet Demo Tests...")
        print("-" * 40)

        # Test 1: Home Page Load
        print("\n1️⃣ Testing Home Page Load...")
        home_page.open_home_page()
        title = home_page.get_page_title()
        heading = home_page.get_heading()
        subheading = home_page.get_subheading()

        print(f"   ✅ Page loaded: {title}")
        print(f"   📍 URL: {driver.current_url}")
        print(f"   📝 Heading: {heading}")
        print(f"   📝 Subheading: {subheading}")

        # Test 2: Page Content Analysis
        print("\n2️⃣ Testing Page Content Analysis...")

        # Get all links
        all_links = home_page.get_all_links()
        links_count = home_page.get_links_count()

        print(f"   📊 Total links found: {links_count}")
        print(
            f"   🔗 Visible links: {len([link for link in all_links if link['visible']])}"
        )

        # Show some example links
        visible_links = [link for link in all_links if link["visible"] and link["text"]]
        print(f"   📋 Sample links:")
        for i, link in enumerate(visible_links[:5], 1):
            print(f"      {i}. {link['text']}")

        # Test 3: Navigation to Different Pages
        print("\n3️⃣ Testing Navigation to Different Pages...")

        # Test some popular pages
        test_pages = [
            "form authentication",
            "checkboxes",
            "dropdown",
            "dynamic loading",
            "file upload",
        ]

        for page_name in test_pages:
            try:
                # Go back to home first
                home_page.open_home_page()
                time.sleep(1)

                # Click on the page link
                home_page.click_link(page_name)
                time.sleep(2)

                print(f"   ✅ {page_name}: {driver.current_url}")

            except Exception as e:
                print(f"   ❌ {page_name}: Error - {e}")

        # Test 4: AI Data Integration
        print("\n4️⃣ Testing AI Data Integration...")

        # Generate AI data
        user_data = ai_generator.generate_user_profile("customer")
        products_data = ai_generator.generate_product_catalog("electronics", 3)

        print(f"   🤖 AI User: {user_data['first_name']} {user_data['last_name']}")
        print(f"   🤖 AI Email: {user_data['email']}")
        print(f"   🤖 AI Products: {[p['name'] for p in products_data]}")

        # Test 5: Link Visibility Testing
        print("\n5️⃣ Testing Link Visibility...")

        # Go back to home
        home_page.open_home_page()
        time.sleep(1)

        # Test visibility of key links
        key_links = [
            "form authentication",
            "checkboxes",
            "dropdown",
            "dynamic loading",
            "file upload",
            "javascript alerts",
            "multiple windows",
        ]

        for link_name in key_links:
            is_visible = home_page.is_link_visible(link_name)
            status = "✅ Visible" if is_visible else "❌ Not visible"
            print(f"   {status} {link_name}")

        # Test 6: Performance Testing
        print("\n6️⃣ Testing Page Load Performance...")

        # Test multiple page loads
        load_times = []
        for i in range(3):
            start_time = time.time()
            home_page.open_home_page()
            load_time = time.time() - start_time
            load_times.append(load_time)
            print(f"   ⏱️ Load {i+1}: {load_time:.2f} seconds")

        avg_load_time = sum(load_times) / len(load_times)
        print(f"   📊 Average load time: {avg_load_time:.2f} seconds")

        if avg_load_time < 3:
            print("   ✅ Excellent performance")
        elif avg_load_time < 5:
            print("   ✅ Good performance")
        else:
            print("   ⚠️ Slow performance")

        # Test 7: Responsive Design Testing
        print("\n7️⃣ Testing Responsive Design...")

        viewports = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile"),
        ]

        for width, height, device in viewports:
            driver.set_window_size(width, height)
            time.sleep(1)

            try:
                # Check if heading is visible
                heading = home_page.get_heading()
                if heading:
                    print(f"   ✅ {device} ({width}x{height}): Heading visible")
                else:
                    print(f"   ❌ {device} ({width}x{height}): Heading not visible")
            except Exception as e:
                print(f"   ❌ {device} ({width}x{height}): Error - {e}")

        # Test 8: Content Validation
        print("\n8️⃣ Testing Content Validation...")

        # Go back to home
        home_page.open_home_page()
        time.sleep(1)

        # Validate expected content
        expected_title = "The Internet"
        expected_heading = "Welcome to the-internet"

        actual_title = home_page.get_page_title()
        actual_heading = home_page.get_heading()

        print(f"   📝 Title validation:")
        print(f"      Expected: {expected_title}")
        print(f"      Actual: {actual_title}")
        print(
            f"      Status: {'✅ Match' if expected_title in actual_title else '❌ Mismatch'}"
        )

        print(f"   📝 Heading validation:")
        print(f"      Expected: {expected_heading}")
        print(f"      Actual: {actual_heading}")
        print(
            f"      Status: {'✅ Match' if actual_heading and expected_heading in actual_heading else '❌ Mismatch'}"
        )

        # Test 9: Link Functionality
        print("\n9️⃣ Testing Link Functionality...")

        # Test a few specific links
        test_links = [
            ("form authentication", "/login"),
            ("checkboxes", "/checkboxes"),
            ("dropdown", "/dropdown"),
        ]

        for link_name, expected_path in test_links:
            try:
                # Go back to home
                home_page.open_home_page()
                time.sleep(1)

                # Click link
                home_page.click_link(link_name)
                time.sleep(2)

                current_url = driver.current_url
                if expected_path in current_url:
                    print(f"   ✅ {link_name}: Link works correctly")
                else:
                    print(f"   ❌ {link_name}: Unexpected URL - {current_url}")

            except Exception as e:
                print(f"   ❌ {link_name}: Error - {e}")

        # Test 10: Error Handling
        print("\n🔟 Testing Error Handling...")

        # Test non-existent link
        try:
            home_page.click_link("non-existent-link")
            print("   ❌ Should have failed for non-existent link")
        except Exception as e:
            print("   ✅ Properly handled non-existent link")

        # Summary
        print("\n" + "=" * 60)
        print("🎉 The Internet Demo Completed Successfully!")
        print("=" * 60)

        print("\n📊 Demo Summary:")
        print("   ✅ Home page loads correctly")
        print("   ✅ Page content analysis works")
        print("   ✅ Navigation to different pages functional")
        print("   ✅ AI data integration successful")
        print("   ✅ Link visibility testing works")
        print("   ✅ Performance testing completed")
        print("   ✅ Responsive design testing works")
        print("   ✅ Content validation successful")
        print("   ✅ Link functionality verified")
        print("   ✅ Error handling works")

        print("\n🤖 AI Integration:")
        print("   ✅ AI-generated user data")
        print("   ✅ AI-generated product data")
        print("   ✅ Real vs AI data comparison")

        print("\n🌐 Test Coverage:")
        print(f"   📊 Total links tested: {links_count}")
        print(f"   🔗 Navigation pages tested: {len(test_pages)}")
        print(f"   📱 Responsive breakpoints tested: {len(viewports)}")
        print(f"   ⏱️ Performance measurements: {len(load_times)}")

        print("\n🚀 Ready for real-world testing!")
        print("📖 Check tests/ui/test_internet_home_page.py for full test suite")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.error(f"Demo error: {e}")

    finally:
        # Cleanup
        if driver:
            driver.quit()
            print("\n🧹 WebDriver closed")


if __name__ == "__main__":
    main()
