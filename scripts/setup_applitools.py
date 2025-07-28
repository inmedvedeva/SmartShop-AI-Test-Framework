#!/usr/bin/env python3
"""
Setup script for Applitools Eyes
Helps configure API key and test connection
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def setup_applitools():
    """Setup Applitools API key and test connection"""

    print("🤖 Applitools Eyes Setup")
    print("=" * 50)

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please copy config/environments/env_example.txt to .env first")
        return False

    # Read current .env file
    with open(env_file) as f:
        content = f.read()

    # Check if API key is already set
    if "APPLITOOLS_API_KEY=your-applitools-api-key-here" in content:
        print("📝 Applitools API key not configured yet")
        print("\nTo get your API key:")
        print("1. Visit https://applitools.com/")
        print("2. Sign up for a free account")
        print("3. Go to your account settings")
        print("4. Copy your API key")
        print("\nThen edit .env file and replace:")
        print("APPLITOOLS_API_KEY=your-applitools-api-key-here")
        print("with your actual API key")

        api_key = input(
            "\nEnter your Applitools API key (or press Enter to skip): "
        ).strip()

        if api_key:
            # Update .env file
            new_content = content.replace(
                "APPLITOOLS_API_KEY=your-applitools-api-key-here",
                f"APPLITOOLS_API_KEY={api_key}",
            )

            with open(env_file, "w") as f:
                f.write(new_content)

            print("✅ API key saved to .env file")

            # Test connection
            return test_applitools_connection(api_key)
        else:
            print("⏭️ Skipping API key setup")
            return False

    else:
        print("✅ Applitools API key already configured")
        # Extract API key from .env
        for line in content.split("\n"):
            if line.startswith("APPLITOOLS_API_KEY="):
                api_key = line.split("=")[1]
                return test_applitools_connection(api_key)

    return False


def test_applitools_connection(api_key):
    """Test Applitools connection"""

    print("\n🔍 Testing Applitools connection...")

    try:
        # Set environment variable
        os.environ["APPLITOOLS_API_KEY"] = api_key

        # Try to import and initialize Applitools
        from src.core.utils.visual_testing import VisualTester

        visual_tester = VisualTester()

        if visual_tester.eyes:
            print("✅ Applitools connection successful!")
            print("🎉 You can now use visual testing features")
            return True
        else:
            print("❌ Applitools not available")
            print("Make sure you have installed: pip install eyes-selenium")
            return False

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed: pip install eyes-selenium")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Please check your API key and internet connection")
        return False


def show_applitools_info():
    """Show information about Applitools"""

    print("\n📚 Applitools Eyes Information")
    print("=" * 50)

    print("🎯 What is Applitools Eyes?")
    print("   - AI-powered visual testing platform")
    print("   - Automatically detects visual regressions")
    print("   - Works with Selenium, Playwright, and other tools")
    print("   - Provides detailed visual comparison reports")

    print("\n🚀 Key Features:")
    print("   ✅ AI-powered image analysis")
    print("   ✅ Automatic baseline management")
    print("   ✅ Cross-browser testing")
    print("   ✅ Responsive design testing")
    print("   ✅ CI/CD integration")
    print("   ✅ Detailed reporting")

    print("\n💡 How it works:")
    print("   1. Takes screenshots of your application")
    print("   2. Compares with baseline images")
    print("   3. Uses AI to analyze differences")
    print("   4. Ignores minor changes (animations, time)")
    print("   5. Flags critical UI changes")

    print("\n🔗 Useful Links:")
    print("   - Website: https://applitools.com/")
    print("   - Documentation: https://applitools.com/docs/")
    print("   - Free Trial: https://applitools.com/trial/")


def main():
    """Main setup function"""

    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        show_applitools_info()
        return

    print("Welcome to Applitools Eyes setup!")
    print("This script will help you configure visual testing with Applitools")

    success = setup_applitools()

    if success:
        print("\n🎉 Setup completed successfully!")
        print("You can now run visual tests with:")
        print("   pytest tests/visual/")
        print("   python examples/applitools_example.py")
    else:
        print("\n⚠️ Setup incomplete")
        print("You can still use the framework without Applitools")
        print("Visual testing will fall back to basic screenshot comparison")

    print("\nFor more information, run: python scripts/setup_applitools.py --info")


if __name__ == "__main__":
    main()
