"""
SmartShop AI Test Framework
===========================

Comprehensive test framework for demonstrating Automation QA Engineer skills.

Key Features:
- UI testing with Selenium/Playwright
- API testing with requests
- AI-powered test data generation
- Visual testing with Applitools
- CI/CD integration with GitHub Actions
- Docker containerization
- Allure reports

Author: Automation QA Engineer
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Automation QA Engineer"
__email__ = "qa@smartshop.com"

# Imports for convenience
from src.core.config.settings import get_settings, settings
from src.core.utils.ai_data_generator import AIDataGenerator
from src.core.utils.visual_testing import VisualTester

# Main classes for quick access
__all__ = ["settings", "get_settings", "AIDataGenerator", "VisualTester"]
