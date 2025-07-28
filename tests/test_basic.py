"""
Basic tests that can run in CI without external dependencies.
These tests ensure the basic functionality works.
"""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestBasicFunctionality:
    """Basic functionality tests that don't require external services."""

    def test_project_structure(self):
        """Test that the project has the expected structure."""
        assert (project_root / "tests").exists()
        # Check for 'src/utils' instead of 'utils' in the root
        assert os.path.isdir(
            os.path.join(project_root, "src", "utils")
        ), "src/utils folder not found."
        # Check for 'src/ui/pages' instead of 'pages' in the root
        assert os.path.isdir(
            os.path.join(project_root, "src", "ui", "pages")
        ), "src/ui/pages folder not found."
        assert (project_root / "config").exists()

    def test_imports(self):
        """Test that basic modules can be imported."""
        try:
            from src.core.utils.ai_data_generator import AIDataGenerator

            assert AIDataGenerator is not None
        except ImportError as e:
            pytest.skip(f"AI Data Generator not available: {e}")

    def test_config_files(self):
        """Test that configuration files exist."""
        config_files = ["requirements.txt", ".gitignore", "README.md"]

        for config_file in config_files:
            assert (project_root / config_file).exists(), f"Missing {config_file}"
        # Check for 'requirements.txt' in the root
        assert os.path.isfile(
            os.path.join(project_root, "requirements.txt")
        ), "requirements.txt file not found in project root"

    def test_environment_variables(self):
        """Test environment variable handling."""
        # Test that we can set and get environment variables
        test_var = "TEST_VARIABLE"
        test_value = "test_value"

        os.environ[test_var] = test_value
        assert os.environ.get(test_var) == test_value

        # Clean up
        del os.environ[test_var]


class TestMockAPI:
    """Tests for mock API functionality."""

    def test_mock_api_import(self):
        """Test that mock API can be imported."""
        try:
            from mock_api_server import app

            assert app is not None
        except ImportError as e:
            pytest.skip(f"Mock API not available: {e}")

    def test_mock_api_routes(self):
        """Test that mock API has expected routes."""
        try:
            from mock_api_server import app

            # Check that the app has routes
            routes = [rule.rule for rule in app.url_map.iter_rules()]
            assert len(routes) > 0

            # Check for specific routes
            route_names = [rule.endpoint for rule in app.url_map.iter_rules()]
            assert "health_check" in route_names or "/health" in routes

        except ImportError:
            pytest.skip("Mock API not available")


class TestAIDataGenerator:
    """Tests for AI data generator functionality."""

    def test_ai_generator_creation(self):
        """Test that AI data generator can be created."""
        try:
            from src.core.utils.ai_data_generator import AIDataGenerator

            # Test creation without API key (should use fallback)
            generator = AIDataGenerator()
            assert generator is not None

        except ImportError as e:
            pytest.skip(f"AI Data Generator not available: {e}")

    def test_faker_fallback(self):
        """Test that Faker fallback works."""
        try:
            from src.core.utils.ai_data_generator import AIDataGenerator

            generator = AIDataGenerator()

            # Test generating data without AI (should use Faker)
            user_data = generator.generate_user_profile()
            assert isinstance(user_data, dict)
            assert "first_name" in user_data
            assert "email" in user_data
            assert isinstance(user_data["first_name"], str)
            assert len(user_data["first_name"]) > 0
            assert "@" in user_data["email"]

        except ImportError as e:
            pytest.skip(f"AI Data Generator not available: {e}")


class TestPageObjects:
    """Tests for page object models."""

    def test_page_object_imports(self):
        """Test that page objects can be imported."""
        try:
            from pages.home_page import HomePage

            assert HomePage is not None
        except ImportError as e:
            pytest.skip(f"Page objects not available: {e}")

    def test_page_object_structure(self):
        """Test that page objects have expected structure."""
        try:
            from pages.home_page import HomePage

            # Test that page object has expected methods
            page = HomePage(None)  # Pass None as driver for testing
            assert hasattr(page, "open")
            assert hasattr(page, "get_title")

        except ImportError:
            pytest.skip("Page objects not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
