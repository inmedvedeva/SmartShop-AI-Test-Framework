#!/usr/bin/env python3
"""
Main entry point for SmartShop AI Test Framework
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.config.settings import settings
from src.version import __version__


def main():
    """Main function"""
    print(f"SmartShop AI Test Framework v{__version__}")
    print(f"Base URL: {settings.base_url}")
    print(f"Browser: {settings.browser_type}")
    print(f"Headless: {settings.headless_mode}")

    # Initialize AI data generator
    print("Initializing AI data generator...")

    # Import and start mock API server if needed
    try:
        from src.api.mock_api_server import app  # noqa: F401

        print("Mock API server available")
    except ImportError:
        print("Mock API server not available")

    print("Framework initialized successfully!")


if __name__ == "__main__":
    main()
