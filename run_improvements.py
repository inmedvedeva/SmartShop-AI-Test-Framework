#!/usr/bin/env python3
"""
SmartShop AI Test Framework - Improvements Verification Script
Runs all improvements and verifies they work correctly
"""
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ImprovementsRunner:
    """Runs and verifies all framework improvements"""

    def __init__(self):
        self.project_root = Path(".")
        self.results = {}

    def run_command(self, command: str, description: str) -> bool:
        """Run a command and return success status"""
        print(f"\n🔄 {description}")
        print(f"   Command: {command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                print(f"   ✅ Success")
                if result.stdout.strip():
                    print(f"   Output: {result.stdout.strip()}")
                return True
            else:
                print(f"   ❌ Failed")
                if result.stderr.strip():
                    print(f"   Error: {result.stderr.strip()}")
                return False

        except Exception as e:
            print(f"   ❌ Exception: {e}")
            return False

    def check_file_exists(self, filepath: str, description: str) -> bool:
        """Check if a file exists"""
        full_path = self.project_root / filepath
        exists = full_path.exists()

        print(f"\n📁 {description}")
        print(f"   File: {filepath}")

        if exists:
            print(f"   ✅ Exists")
            return True
        else:
            print(f"   ❌ Missing")
            return False

    def check_file_content(
        self, filepath: str, expected_content: str, description: str
    ) -> bool:
        """Check if file contains expected content"""
        full_path = self.project_root / filepath

        print(f"\n📄 {description}")
        print(f"   File: {filepath}")

        if not full_path.exists():
            print(f"   ❌ File not found")
            return False

        try:
            with open(full_path, encoding="utf-8") as f:
                content = f.read()

            if expected_content in content:
                print(f"   ✅ Contains expected content")
                return True
            else:
                print(f"   ❌ Missing expected content")
                return False

        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            return False

    def verify_readme(self) -> bool:
        """Verify README.md improvements"""
        print("\n" + "=" * 60)
        print("📖 VERIFYING README.md IMPROVEMENTS")
        print("=" * 60)

        success = True

        # Check if README exists
        success &= self.check_file_exists("README.md", "README.md file exists")

        # Check for key sections
        expected_sections = [
            "SmartShop AI Test Framework",
            "Features",
            "Installation",
            "Configuration",
            "Running Tests",
            "Reports",
            "AI Features",
            "Docker Support",
            "Development",
            "CI/CD",
            "Troubleshooting",
        ]

        for section in expected_sections:
            success &= self.check_file_content(
                "README.md", section, f"README contains '{section}' section"
            )

        return success

    def verify_pre_commit(self) -> bool:
        """Verify pre-commit configuration"""
        print("\n" + "=" * 60)
        print("🔧 VERIFYING PRE-COMMIT CONFIGURATION")
        print("=" * 60)

        success = True

        # Check pre-commit config file
        success &= self.check_file_exists(
            ".pre-commit-config.yaml", "Pre-commit config file exists"
        )

        # Check for key hooks
        expected_hooks = ["black", "isort", "flake8", "mypy", "bandit"]
        for hook in expected_hooks:
            success &= self.check_file_content(
                ".pre-commit-config.yaml",
                hook,
                f"Pre-commit config contains {hook} hook",
            )

        # Test pre-commit installation
        success &= self.run_command("pre-commit --version", "Pre-commit is installed")

        return success

    def verify_openai_config(self) -> bool:
        """Verify OpenAI configuration improvements"""
        print("\n" + "=" * 60)
        print("🤖 VERIFYING OPENAI CONFIGURATION")
        print("=" * 60)

        success = True

        # Check settings file for new OpenAI options
        expected_settings = [
            "openai_model",
            "openai_max_tokens",
            "openai_temperature",
            "openai_timeout",
        ]

        for setting in expected_settings:
            success &= self.check_file_content(
                "config/settings.py", setting, f"Settings contains {setting}"
            )

        # Check env example
        expected_env_vars = [
            "OPENAI_MODEL",
            "OPENAI_MAX_TOKENS",
            "OPENAI_TEMPERATURE",
            "OPENAI_TIMEOUT",
        ]

        for var in expected_env_vars:
            success &= self.check_file_content(
                "env_example.txt", var, f"Env example contains {var}"
            )

        return success

    def verify_unit_tests(self) -> bool:
        """Verify unit tests for AI generator"""
        print("\n" + "=" * 60)
        print("🧪 VERIFYING UNIT TESTS")
        print("=" * 60)

        success = True

        # Check if unit test file exists
        success &= self.check_file_exists(
            "tests/unit/test_ai_data_generator.py", "AI generator unit tests exist"
        )

        # Check for key test methods
        expected_tests = [
            "test_init_without_openai_key",
            "test_generate_user_profile_with_faker_fallback",
            "test_generate_user_profile_with_ai_403_error",
            "test_generate_user_profile_with_ai_401_error",
            "test_generate_user_profile_with_ai_429_error",
        ]

        for test in expected_tests:
            success &= self.check_file_content(
                "tests/unit/test_ai_data_generator.py",
                test,
                f"Unit tests contain {test}",
            )

        return success

    def verify_constants(self) -> bool:
        """Verify constants file"""
        print("\n" + "=" * 60)
        print("📋 VERIFYING CONSTANTS FILE")
        print("=" * 60)

        success = True

        # Check if constants file exists
        success &= self.check_file_exists("utils/constants.py", "Constants file exists")

        # Check for key constant categories
        expected_constants = [
            "COMMON_LOCATORS",
            "FORM_LOCATORS",
            "NAVIGATION_LOCATORS",
            "USER_TYPES",
            "PRODUCT_CATEGORIES",
            "TEST_DATA",
            "API_ENDPOINTS",
            "HTTP_STATUS_CODES",
            "LOG_MESSAGES",
            "ERROR_MESSAGES",
            "AI_PROMPTS",
            "OPENAI_ERROR_CODES",
        ]

        for constant in expected_constants:
            success &= self.check_file_content(
                "utils/constants.py", constant, f"Constants file contains {constant}"
            )

        return success

    def verify_coverage_audit(self) -> bool:
        """Verify coverage audit script"""
        print("\n" + "=" * 60)
        print("📊 VERIFYING COVERAGE AUDIT")
        print("=" * 60)

        success = True

        # Check if audit script exists
        success &= self.check_file_exists(
            "tests/coverage_audit.py", "Coverage audit script exists"
        )

        # Check for key audit methods
        expected_methods = [
            "scan_project",
            "analyze_test_structure",
            "analyze_source_coverage",
            "analyze_code_complexity",
            "generate_recommendations",
        ]

        for method in expected_methods:
            success &= self.check_file_content(
                "tests/coverage_audit.py", method, f"Audit script contains {method}"
            )

        # Run coverage audit
        success &= self.run_command(
            "python tests/coverage_audit.py", "Coverage audit runs successfully"
        )

        # Check if report was generated
        success &= self.check_file_exists(
            "reports/coverage_audit_report.json", "Coverage audit report generated"
        )

        return success

    def verify_ci_cd_improvements(self) -> bool:
        """Verify CI/CD improvements"""
        print("\n" + "=" * 60)
        print("🚀 VERIFYING CI/CD IMPROVEMENTS")
        print("=" * 60)

        success = True

        # Check for GitHub Pages deployment
        success &= self.check_file_content(
            ".github/workflows/test-runner.yml",
            "Deploy Allure Report to GitHub Pages",
            "CI/CD contains GitHub Pages deployment",
        )

        # Check for PR comments
        success &= self.check_file_content(
            ".github/workflows/test-runner.yml",
            "Comment PR with Test Results",
            "CI/CD contains PR comment functionality",
        )

        return success

    def run_tests(self) -> bool:
        """Run a subset of tests to verify everything works"""
        print("\n" + "=" * 60)
        print("🧪 RUNNING VERIFICATION TESTS")
        print("=" * 60)

        success = True

        # Run unit tests
        success &= self.run_command(
            "python -m pytest tests/unit/ -v", "Unit tests pass"
        )

        # Run a few smoke tests
        success &= self.run_command(
            "python -m pytest tests/ -m smoke -v", "Smoke tests pass"
        )

        return success

    def run_all_verifications(self) -> dict[str, bool]:
        """Run all verification checks"""
        print("🚀 SMART SHOP AI TEST FRAMEWORK - IMPROVEMENTS VERIFICATION")
        print("=" * 80)

        verifications = {
            "README Improvements": self.verify_readme(),
            "Pre-commit Configuration": self.verify_pre_commit(),
            "OpenAI Configuration": self.verify_openai_config(),
            "Unit Tests": self.verify_unit_tests(),
            "Constants File": self.verify_constants(),
            "Coverage Audit": self.verify_coverage_audit(),
            "CI/CD Improvements": self.verify_ci_cd_improvements(),
            "Test Execution": self.run_tests(),
        }

        # Print summary
        print("\n" + "=" * 80)
        print("📋 VERIFICATION SUMMARY")
        print("=" * 80)

        all_passed = True
        for name, result in verifications.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{name:<30} {status}")
            if not result:
                all_passed = False

        print("\n" + "=" * 80)
        if all_passed:
            print("🎉 ALL IMPROVEMENTS VERIFIED SUCCESSFULLY!")
        else:
            print("⚠️ SOME VERIFICATIONS FAILED - CHECK ABOVE FOR DETAILS")
        print("=" * 80)

        return verifications


def main():
    """Main function"""
    runner = ImprovementsRunner()
    results = runner.run_all_verifications()

    # Exit with appropriate code
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
