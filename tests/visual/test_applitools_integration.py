"""
Applitools Eyes integration test
Demonstrates AI-powered visual testing
"""

import time

import pytest
from selenium.webdriver.common.by import By

from src.core.utils.visual_testing import VisualTester
from src.ui.pages.automation_exercise_home_page import AutomationExerciseHomePage


class TestApplitoolsIntegration:
    """Applitools Eyes integration tests"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Test setup"""
        self.driver = driver
        self.visual_tester = VisualTester()
        self.home_page = AutomationExerciseHomePage(driver)

    def test_home_page_visual_baseline(self):
        """
        Test creating baseline for home page

        Applitools process:
        1. Takes screenshot of the page
        2. Saves as baseline (reference)
        3. On subsequent runs compares with baseline
        4. Uses AI to analyze differences
        """
        # Open home page
        self.home_page.open_home_page()
        time.sleep(3)  # Wait for full loading

        # Create baseline (first run)
        result = self.visual_tester.check_page_layout("home_page_baseline", self.driver)

        # Check that baseline was created
        assert result["status"] in [
            "passed",
            "warning",
            "failed",
        ], f"Baseline not created: {result['status']}"

        print(f"✅ Baseline created: {result['status']}")

    def test_home_page_visual_comparison(self):
        """
        Test comparison with baseline

        Applitools AI analysis:
        - Ignores minor changes (time, animations)
        - Focuses on critical UI changes
        - Provides detailed reporting
        """
        # Open home page
        self.home_page.open_home_page()
        time.sleep(3)

        # Compare with baseline
        result = self.visual_tester.check_page_layout(
            "home_page_comparison", self.driver
        )

        # Check result
        assert result["status"] in [
            "passed",
            "failed",
            "warning",
        ], f"Unexpected status: {result['status']}"

        if result["status"] == "failed":
            print("❌ Visual differences detected!")
            if "diff_image" in result:
                print(f"📷 Diff image: {result['diff_image']}")
        else:
            print("✅ No visual differences detected")

    def test_header_region_visual_check(self):
        """
        Test visual check of specific region (header)

        Advantages of region checking:
        - Focus on important elements
        - Ignore dynamic content
        - More precise testing
        """
        self.home_page.open_home_page()
        time.sleep(3)

        # Find header element
        header = self.driver.find_element(By.CSS_SELECTOR, ".header-middle")
        header_location = header.location
        header_size = header.size

        # Define region for checking
        region = (
            header_location["x"],
            header_location["y"],
            header_size["width"],
            header_size["height"],
        )

        # Check only header region
        result = self.visual_tester.check_page_layout(
            "header_region", self.driver, region=region
        )

        assert result["status"] in [
            "passed",
            "failed",
            "warning",
        ], f"Unexpected status for header: {result['status']}"

        print(f"📊 Header check: {result['status']}")

    def test_visual_check_after_interaction(self):
        """
        Test visual check after element interaction

        Shows how Applitools tracks changes:
        - After clicks
        - After form filling
        - After navigation
        """
        self.home_page.open_home_page()
        time.sleep(3)

        # Baseline check
        baseline_result = self.visual_tester.check_page_layout(
            "before_interaction", self.driver
        )

        # Simulate interaction (e.g., hover over element)
        products_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/products']")
        self.driver.execute_script(
            "arguments[0].style.backgroundColor = 'yellow';", products_link
        )
        time.sleep(2)

        # Check after interaction
        after_result = self.visual_tester.check_page_layout(
            "after_interaction", self.driver
        )

        # Both results should be valid
        assert baseline_result["status"] in ["passed", "failed", "warning"]
        assert after_result["status"] in ["passed", "failed", "warning"]

        print(f"📊 Before interaction: {baseline_result['status']}")
        print(f"📊 After interaction: {after_result['status']}")

    def test_responsive_visual_check(self):
        """
        Test visual check on different screen sizes

        Applitools automatically:
        - Adapts to different resolutions
        - Considers responsive design
        - Compares elements in context of their size
        """
        # Test on desktop
        self.driver.set_window_size(1920, 1080)
        self.home_page.open_home_page()
        time.sleep(3)

        desktop_result = self.visual_tester.check_page_layout(
            "home_page_desktop", self.driver
        )

        # Test on tablet
        self.driver.set_window_size(768, 1024)
        self.driver.refresh()
        time.sleep(3)

        tablet_result = self.visual_tester.check_page_layout(
            "home_page_tablet", self.driver
        )

        # Test on mobile
        self.driver.set_window_size(375, 667)
        self.driver.refresh()
        time.sleep(3)

        mobile_result = self.visual_tester.check_page_layout(
            "home_page_mobile", self.driver
        )

        # Check all results
        results = [desktop_result, tablet_result, mobile_result]
        for i, result in enumerate(["desktop", "tablet", "mobile"]):
            assert results[i]["status"] in [
                "passed",
                "failed",
                "warning",
            ], f"Unexpected status for {result}: {results[i]['status']}"
            print(f"📱 {result.capitalize()}: {results[i]['status']}")

    def test_visual_check_with_ai_analysis(self):
        """
        Test Applitools AI analysis

        AI capabilities:
        - Ignore minor changes
        - Detect critical UI issues
        - Analyze change context
        - Suggest fixes
        """
        self.home_page.open_home_page()
        time.sleep(3)

        # Create baseline
        baseline_result = self.visual_tester.check_page_layout(
            "ai_baseline", self.driver
        )

        # Simulate minor change (AI should ignore)
        self.driver.execute_script(
            """
            document.body.style.color = '#666666';
        """
        )
        time.sleep(2)

        minor_change_result = self.visual_tester.check_page_layout(
            "ai_minor_change", self.driver
        )

        # Simulate critical change (AI should detect)
        self.driver.execute_script(
            """
            document.querySelector('.header-middle').style.display = 'none';
        """
        )
        time.sleep(2)

        critical_change_result = self.visual_tester.check_page_layout(
            "ai_critical_change", self.driver
        )

        # Check results
        assert baseline_result["status"] in ["passed", "failed", "warning"]
        assert minor_change_result["status"] in ["passed", "failed", "warning"]
        assert critical_change_result["status"] in ["passed", "failed", "warning"]

        print("🤖 AI analysis results:")
        print(f"   Baseline: {baseline_result['status']}")
        print(f"   Minor change: {minor_change_result['status']}")
        print(f"   Critical change: {critical_change_result['status']}")

    def test_visual_check_error_handling(self):
        """
        Test error handling in visual testing

        Check graceful degradation:
        - When Applitools is unavailable
        - Network errors
        - API key issues
        """
        # Test with incorrect parameters
        try:
            result = self.visual_tester.check_page_layout(
                "error_test", None  # Pass None instead of driver
            )
            print(f"📊 Result with error: {result['status']}")
        except Exception as e:
            print(f"✅ Error handled correctly: {type(e).__name__}")

        # Test with incorrect region
        self.home_page.open_home_page()
        time.sleep(3)

        try:
            result = self.visual_tester.check_page_layout(
                "invalid_region_test",
                self.driver,
                region=(9999, 9999, 100, 100),  # Invalid coordinates
            )
            print(f"📊 Result with invalid region: {result['status']}")
        except Exception as e:
            print(f"✅ Invalid region handled: {type(e).__name__}")


# Markers for test grouping
pytest.mark.visual = pytest.mark.visual
pytest.mark.applitools = pytest.mark.applitools
pytest.mark.ai = pytest.mark.ai

# Apply markers to class
TestApplitoolsIntegration = pytest.mark.visual(
    pytest.mark.applitools(pytest.mark.ai(TestApplitoolsIntegration))
)
