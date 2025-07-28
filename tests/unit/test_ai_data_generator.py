"""
Unit tests for AI Data Generator
Tests fallback logic and error handling
"""

import os
from unittest.mock import MagicMock, Mock, patch

from src.core.utils.ai_data_generator import AIDataGenerator


class TestAIDataGenerator:
    """Unit tests for AIDataGenerator class"""

    def test_init_without_openai_key(self):
        """Test initialization without OpenAI API key"""
        # Mock settings to return None for API key
        with patch("src.core.utils.ai_data_generator.settings") as mock_settings:
            mock_settings.openai_api_key = None

            generator = AIDataGenerator()
            assert generator.openai_client is None

    def test_init_with_invalid_openai_key(self):
        """Test initialization with invalid OpenAI API key"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key"}):
            # The generator will still create a client, but it will fail when used
            generator = AIDataGenerator()
            # The client is created but will fail on actual API calls
            assert generator.openai_client is not None

    def test_init_with_valid_openai_key(self):
        """Test initialization with valid OpenAI API key"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-valid-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                assert generator.openai_client is not None
                mock_openai.assert_called_once()

    def test_generate_user_profile_with_faker_fallback(self):
        """Test user profile generation with Faker fallback"""
        generator = AIDataGenerator()
        generator.openai_client = None  # Force Faker fallback

        user = generator.generate_user_profile("customer")

        # Check that user has all required fields
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "postal_code",
            "date_of_birth",
            "preferences",
            "loyalty_points",
            "registration_date",
        ]

        for field in required_fields:
            assert field in user, f"Missing field: {field}"
            assert user[field] is not None, f"Field {field} is None"

    def test_generate_user_profile_with_ai_success(self):
        """Test user profile generation with AI success"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = """
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "address": "123 Main St",
            "city": "New York",
            "country": "USA",
            "postal_code": "10001",
            "date_of_birth": "1990-01-01",
            "preferences": ["electronics", "books"],
            "loyalty_points": 150,
            "registration_date": "2023-01-01"
        }
        """

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                user = generator.generate_user_profile("customer")

                assert user["first_name"] == "John"
                assert user["last_name"] == "Doe"
                assert user["email"] == "john.doe@example.com"

    def test_generate_user_profile_with_ai_403_error(self):
        """Test user profile generation with AI 403 error (geographic restriction)"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = """
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "address": "123 Main St",
            "city": "New York",
            "country": "USA",
            "postal_code": "10001",
            "date_of_birth": "1990-01-01",
            "preferences": ["electronics", "books"],
            "loyalty_points": 150,
            "registration_date": "2023-01-01"
        }
        """

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                # Simulate 403 error
                mock_client.chat.completions.create.side_effect = Exception(
                    "Error code: 403 - {'error': {'code': 'unsupported_country_region_territory'}}"
                )
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                user = generator.generate_user_profile("customer")

                # Should fallback to Faker
                assert "first_name" in user
                assert "last_name" in user
                assert "email" in user

    def test_generate_user_profile_with_ai_401_error(self):
        """Test user profile generation with AI 401 error (invalid API key)"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-invalid-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                # Simulate 401 error
                mock_client.chat.completions.create.side_effect = Exception(
                    "Error code: 401 - {'error': {'code': 'invalid_api_key'}}"
                )
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                user = generator.generate_user_profile("customer")

                # Should fallback to Faker
                assert "first_name" in user
                assert "last_name" in user
                assert "email" in user

    def test_generate_user_profile_with_ai_429_error(self):
        """Test user profile generation with AI 429 error (rate limit)"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                # Simulate 429 error
                mock_client.chat.completions.create.side_effect = Exception(
                    "Error code: 429 - Rate limit exceeded"
                )
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                user = generator.generate_user_profile("customer")

                # Should fallback to Faker
                assert "first_name" in user
                assert "last_name" in user
                assert "email" in user

    def test_generate_product_catalog_with_faker_fallback(self):
        """Test product catalog generation with Faker fallback"""
        generator = AIDataGenerator()
        generator.openai_client = None  # Force Faker fallback

        products = generator.generate_product_catalog("electronics", 3)

        assert len(products) == 3

        for product in products:
            required_fields = [
                "name",
                "description",
                "price",
                "currency",
                "category",
                "brand",
                "sku",
                "stock_quantity",
                "rating",
                "features",
                "images",
            ]

            for field in required_fields:
                assert field in product, f"Missing field: {field}"
                assert product[field] is not None, f"Field {field} is None"

    def test_generate_product_catalog_with_ai_success(self):
        """Test product catalog generation with AI success"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = """
        [
            {
                "name": "Smartphone X",
                "description": "Latest smartphone model",
                "price": 999.99,
                "currency": "USD",
                "category": "electronics",
                "brand": "TechCorp",
                "sku": "SMART-X-001",
                "stock_quantity": 50,
                "rating": 4.5,
                "features": ["5G", "128GB", "Triple Camera"],
                "images": ["https://example.com/phone1.jpg"]
            }
        ]
        """

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                products = generator.generate_product_catalog("electronics", 1)

                assert len(products) == 1
                assert products[0]["name"] == "Smartphone X"
                assert products[0]["price"] == 999.99

    def test_generate_search_terms_with_faker_fallback(self):
        """Test search terms generation with Faker fallback"""
        generator = AIDataGenerator()
        generator.openai_client = None  # Force Faker fallback

        search_terms = generator.generate_search_terms(5)

        assert len(search_terms) == 5
        assert all(isinstance(term, str) for term in search_terms)
        assert all(len(term) > 0 for term in search_terms)

    def test_generate_test_scenarios_with_faker_fallback(self):
        """Test test scenarios generation with Faker fallback"""
        generator = AIDataGenerator()
        generator.openai_client = None  # Force Faker fallback

        scenarios = generator.generate_test_scenarios("search")

        # Should return empty list when OpenAI is not available
        assert scenarios == []

    def test_generate_test_scenarios_with_ai_success(self):
        """Test test scenarios generation with AI success"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = """
        [
            {
                "title": "Search for existing product",
                "description": "Search for a product that exists in catalog",
                "steps": ["Navigate to search page", "Enter product name", "Click search"],
                "expected_result": "Product found and displayed",
                "priority": "high",
                "tags": ["search", "positive"]
            }
        ]
        """

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client

                generator = AIDataGenerator()
                scenarios = generator.generate_test_scenarios("search")

                assert len(scenarios) == 1
                assert scenarios[0]["title"] == "Search for existing product"
                assert scenarios[0]["priority"] == "high"

    def test_different_user_types(self):
        """Test generation of different user types"""
        generator = AIDataGenerator()
        generator.openai_client = None  # Force Faker fallback

        user_types = ["customer", "admin", "vendor"]

        for user_type in user_types:
            user = generator.generate_user_profile(user_type)
            assert "first_name" in user
            assert "last_name" in user
            assert "email" in user

    def test_different_product_categories(self):
        """Test generation of different product categories"""
        generator = AIDataGenerator()
        generator.openai_client = None  # Force Faker fallback

        categories = ["electronics", "clothing", "books", "home", "sports"]

        for category in categories:
            products = generator.generate_product_catalog(category, 2)
            assert len(products) == 2

            for product in products:
                assert product["category"] == category

    def test_configurable_openai_settings(self):
        """Test that OpenAI settings are configurable"""
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "sk-test-key",
                "OPENAI_MODEL": "gpt-4",
                "OPENAI_MAX_TOKENS": "2000",
                "OPENAI_TEMPERATURE": "0.5",
            },
        ):
            with patch("openai.OpenAI") as mock_openai:
                mock_client = Mock()
                mock_response = Mock()
                mock_response.choices = [Mock()]
                mock_response.choices[0].message.content = '{"first_name": "Test"}'
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client

                # Mock the settings to return our test values
                with patch(
                    "src.core.utils.ai_data_generator.settings"
                ) as mock_settings:
                    mock_settings.openai_model = "gpt-4"
                    mock_settings.openai_max_tokens = 2000
                    mock_settings.openai_temperature = 0.5

                    generator = AIDataGenerator()

                    # Test that settings are used
                    generator.generate_user_profile("customer")

                    # Verify that the correct model and parameters were used
                    mock_client.chat.completions.create.assert_called_once()
                    call_args = mock_client.chat.completions.create.call_args

                    assert call_args[1]["model"] == "gpt-4"
                    assert call_args[1]["max_tokens"] == 2000
                    assert call_args[1]["temperature"] == 0.5
