#!/usr/bin/env python3
"""
Simple Test Runner for SmartShop AI Test Framework
Bypasses problematic dependencies and runs core tests
"""
import os
import subprocess
import sys
from pathlib import Path


def run_simple_tests():
    """Run tests with minimal dependencies"""

    # Get project root
    project_root = Path(__file__).parent.absolute()

    # Set up environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    print("🚀 SmartShop AI Test Framework - Simple Test Runner")
    print("=" * 60)

    # Test 1: Health check
    print("\n📋 Test 1: API Health Check")
    print("-" * 30)
    cmd1 = [
        sys.executable,
        "-m",
        "pytest",
        "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_api_health_check",
        "-v",
        "--tb=short",
    ]

    try:
        result1 = subprocess.run(
            cmd1, env=env, cwd=project_root, capture_output=True, text=True
        )
        if result1.returncode == 0:
            print("✅ Health check test PASSED")
        else:
            print("❌ Health check test FAILED")
            print(result1.stdout)
    except Exception as e:
        print(f"❌ Error running health check: {e}")

    # Test 2: Get products
    print("\n📋 Test 2: Get Products")
    print("-" * 30)
    cmd2 = [
        sys.executable,
        "-m",
        "pytest",
        "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_get_products",
        "-v",
        "--tb=short",
    ]

    try:
        result2 = subprocess.run(
            cmd2, env=env, cwd=project_root, capture_output=True, text=True
        )
        if result2.returncode == 0:
            print("✅ Get products test PASSED")
        else:
            print("❌ Get products test FAILED")
            print(result2.stdout)
    except Exception as e:
        print(f"❌ Error running get products: {e}")

    # Test 3: Search products
    print("\n📋 Test 3: Search Products")
    print("-" * 30)
    cmd3 = [
        sys.executable,
        "-m",
        "pytest",
        "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_search_products",
        "-v",
        "--tb=short",
    ]

    try:
        result3 = subprocess.run(
            cmd3, env=env, cwd=project_root, capture_output=True, text=True
        )
        if result3.returncode == 0:
            print("✅ Search products test PASSED")
        else:
            print("❌ Search products test FAILED")
            print(result3.stdout)
    except Exception as e:
        print(f"❌ Error running search products: {e}")

    # Test 4: Create user
    print("\n📋 Test 4: Create User")
    print("-" * 30)
    cmd4 = [
        sys.executable,
        "-m",
        "pytest",
        "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_create_user",
        "-v",
        "--tb=short",
    ]

    try:
        result4 = subprocess.run(
            cmd4, env=env, cwd=project_root, capture_output=True, text=True
        )
        if result4.returncode == 0:
            print("✅ Create user test PASSED")
        else:
            print("❌ Create user test FAILED")
            print(result4.stdout)
    except Exception as e:
        print(f"❌ Error running create user: {e}")

    # Test 5: User login
    print("\n📋 Test 5: User Login")
    print("-" * 30)
    cmd5 = [
        sys.executable,
        "-m",
        "pytest",
        "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_user_login",
        "-v",
        "--tb=short",
    ]

    try:
        result5 = subprocess.run(
            cmd5, env=env, cwd=project_root, capture_output=True, text=True
        )
        if result5.returncode == 0:
            print("✅ User login test PASSED")
        else:
            print("❌ User login test FAILED")
            print(result5.stdout)
    except Exception as e:
        print(f"❌ Error running user login: {e}")

    print("\n" + "=" * 60)
    print("🎯 Simple Test Runner Complete!")
    print("📊 Results: Check individual test outputs above")
    print("\n💡 To run all tests (may have dependency issues):")
    print("   source venv/bin/activate")
    print("   PYTHONPATH=/path/to/project python -m pytest tests/api/ -v")


if __name__ == "__main__":
    run_simple_tests()
