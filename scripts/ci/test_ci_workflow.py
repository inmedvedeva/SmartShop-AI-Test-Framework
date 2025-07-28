#!/usr/bin/env python3
"""
Script to test CI workflow locally before pushing to GitHub.
This script simulates the CI environment and runs basic tests.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(command, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(
        command, shell=True, cwd=cwd, capture_output=True, text=True
    )
    print(f"Exit code: {result.returncode}")
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result


def test_basic_environment():
    """Test basic environment setup."""
    print("=== Testing Basic Environment ===")

    # Check Python version
    result = run_command("python --version")
    if result.returncode != 0:
        print("❌ Python not available")
        return False

    # Check pip
    result = run_command("pip --version")
    if result.returncode != 0:
        print("❌ pip not available")
        return False

    print("✅ Basic environment OK")
    return True


def test_dependencies():
    """Test dependency installation."""
    print("=== Testing Dependencies ===")

    # Install dependencies
    result = run_command("pip install -r requirements.txt")
    if result.returncode != 0:
        print("❌ Failed to install dependencies")
        return False

    print("✅ Dependencies installed successfully")
    return True


def test_basic_tests():
    """Test basic test execution."""
    print("=== Testing Basic Tests ===")

    # Run basic tests
    result = run_command("python -m pytest tests/test_basic.py -v")
    if result.returncode != 0:
        print("❌ Basic tests failed")
        return False

    print("✅ Basic tests passed")
    return True


def test_imports():
    """Test that all modules can be imported."""
    print("=== Testing Imports ===")

    # Test imports
    test_script = """
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from utils.ai_data_generator import AIDataGenerator
    print("✅ AI Data Generator imported successfully")
except ImportError as e:
    print(f"❌ Failed to import AI Data Generator: {e}")

try:
    from pages.home_page import HomePage
    print("✅ Home Page imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Home Page: {e}")

try:
    from mock_api_server import app
    print("✅ Mock API Server imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Mock API Server: {e}")

print("Import test completed")
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_script)
        temp_file = f.name

    try:
        result = run_command(f"python {temp_file}")
        if result.returncode != 0:
            print("❌ Import tests failed")
            return False
    finally:
        os.unlink(temp_file)

    print("✅ All imports successful")
    return True


def test_workflow_file():
    """Test that the workflow file is valid."""
    print("=== Testing Workflow File ===")

    workflow_file = Path(".github/workflows/test-runner.yml")
    if not workflow_file.exists():
        print("❌ Workflow file not found")
        return False

    # Check for deprecated actions
    with open(workflow_file) as f:
        content = f.read()

    deprecated_actions = [
        "actions/upload-artifact@v3",
        "actions/download-artifact@v3",
        "actions/checkout@v3",
        "actions/setup-python@v3",
    ]

    for action in deprecated_actions:
        if action in content:
            print(f"❌ Found deprecated action: {action}")
            return False

    print("✅ Workflow file is valid")
    return True


def main():
    """Main test function."""
    print("🧪 Testing CI Workflow Locally")
    print("=" * 50)

    tests = [
        test_basic_environment,
        test_dependencies,
        test_imports,
        test_basic_tests,
        test_workflow_file,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All tests passed! Ready to push to GitHub.")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before pushing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
