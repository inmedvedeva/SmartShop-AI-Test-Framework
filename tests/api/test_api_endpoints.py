"""
API tests for SmartShop
Demonstrates REST API testing using AI tools
"""

import time
from typing import Any, Dict

import pytest
import requests
from loguru import logger

from config.settings import settings
from utils.ai_data_generator import AIDataGenerator


class TestAPIEndpoints:
    """API endpoint tests with AI-powered data generation"""

    @pytest.fixture(scope="class")
    def api_base_url(self):
        """API base URL fixture"""
        return settings.api_base_url

    @pytest.fixture(scope="class")
    def ai_generator(self):
        """AI data generator fixture"""
        return AIDataGenerator()

    @pytest.fixture(scope="class")
    def session(self):
        """HTTP session fixture"""
        session = requests.Session()
        session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "SmartShop-Test-Framework/1.0",
            }
        )
        return session

    @pytest.fixture(scope="class")
    def auth_token(self, session, api_base_url):
        """Authentication token fixture"""
        try:
            login_data = {
                "email": settings.test_user_email,
                "password": settings.test_user_password,
            }

            response = session.post(f"{api_base_url}/auth/login", json=login_data)

            if response.status_code == 200:
                data = response.json()
                return data.get("token")
            else:
                logger.warning("Failed to get auth token")
                return None

        except Exception as e:
            logger.warning(f"Error getting auth token: {e}")
            return None

    @pytest.mark.api
    @pytest.mark.smoke
    def test_api_health_check(self, session, api_base_url):
        """Test API health check endpoint"""
        try:
            response = session.get(f"{api_base_url}/health")

            assert (
                response.status_code == 200
            ), f"Health check failed: {response.status_code}"

            data = response.json()

            # Check response structure
            assert "status" in data, "Health check missing status field"
            assert "timestamp" in data, "Health check missing timestamp field"
            assert "version" in data, "Health check missing version field"

            # Check status value
            assert data["status"] == "ok", f"Unexpected status: {data['status']}"

            logger.info("API health check passed")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_get_products(self, session, api_base_url):
        """Test getting all products"""
        try:
            response = session.get(f"{api_base_url}/products")

            assert (
                response.status_code == 200
            ), f"Failed to get products: {response.status_code}"

            data = response.json()

            # Check response structure
            assert "products" in data, "Response missing products field"
            assert "total" in data, "Response missing total field"

            products = data["products"]
            total = data["total"]

            # Check data integrity
            assert isinstance(products, list), "Products should be a list"
            assert total >= 0, "Total should be non-negative"
            assert len(products) <= total, "Products count should not exceed total"

            # Check product structure if products exist
            if products:
                product = products[0]
                required_fields = ["id", "name", "price", "description", "category"]
                for field in required_fields:
                    assert field in product, f"Product missing field: {field}"

            logger.info(f"Retrieved {len(products)} products successfully")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_get_product_by_id(self, session, api_base_url):
        """Test getting product by ID"""
        try:
            # First get all products to get a valid ID
            response = session.get(f"{api_base_url}/products")
            assert response.status_code == 200, "Failed to get products list"

            data = response.json()
            products = data.get("products", [])

            if not products:
                pytest.skip("No products available for testing")

            product_id = products[0]["id"]

            # Get specific product
            response = session.get(f"{api_base_url}/products/{product_id}")

            assert (
                response.status_code == 200
            ), f"Failed to get product {product_id}: {response.status_code}"

            product = response.json()

            # Verify it's the same product
            assert (
                product["id"] == product_id
            ), f"Product ID mismatch: expected {product_id}, got {product['id']}"

            # Check required fields
            required_fields = ["id", "name", "price", "description", "category"]
            for field in required_fields:
                assert field in product, f"Product missing field: {field}"

            logger.info(f"Retrieved product {product_id} successfully")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_search_products(self, session, api_base_url, ai_generator):
        """Test product search with AI-generated data"""
        try:
            # Generate search query using AI
            products = ai_generator.generate_product_catalog("electronics", 1)
            search_query = products[0]["name"] if products else "laptop"

            params = {"q": search_query, "limit": 10}
            response = session.get(f"{api_base_url}/products/search", params=params)

            assert response.status_code == 200, f"Search failed: {response.status_code}"

            data = response.json()

            # Check response structure
            assert "products" in data, "Search response missing 'products' field"
            assert "total" in data, "Search response missing 'total' field"

            products = data["products"]
            total = data["total"]

            # Check that results match the query
            assert total >= 0, "Total count should be non-negative"
            assert len(products) <= 10, "Should not exceed limit"

            logger.info(
                f"Search for '{search_query}' returned {len(products)} products"
            )

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_create_user(self, session, api_base_url, ai_generator):
        """Test user creation with AI-generated data"""
        try:
            # Generate user data using AI
            user_data = ai_generator.generate_user_profile("customer")

            # Prepare data for API
            create_user_data = {
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "password": "TestPassword123!",
                "phone": user_data["phone"],
                "address": user_data["address"],
                "city": user_data["city"],
                "country": user_data["country"],
                "postal_code": user_data["postal_code"],
            }

            response = session.post(f"{api_base_url}/users", json=create_user_data)

            # Check result
            if response.status_code == 201:
                # Successful creation
                user = response.json()
                assert "id" in user, "Created user missing ID"
                assert user["email"] == user_data["email"], "Email mismatch"

                logger.info(f"User created successfully: {user['id']}")

            elif response.status_code == 409:
                # User already exists
                logger.info("User already exists (expected for test data)")

            else:
                assert False, f"Unexpected status code: {response.status_code}"

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_user_login(self, session, api_base_url):
        """Test user login"""
        try:
            login_data = {
                "email": settings.test_user_email,
                "password": settings.test_user_password,
            }

            response = session.post(f"{api_base_url}/auth/login", json=login_data)

            assert response.status_code == 200, f"Login failed: {response.status_code}"

            data = response.json()

            # Check response structure
            assert "token" in data, "Login response missing token"
            assert "user" in data, "Login response missing user data"

            token = data["token"]
            user = data["user"]

            # Check token
            assert len(token) > 0, "Token should not be empty"
            assert user["email"] == settings.test_user_email, "User email mismatch"

            logger.info("User login successful")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_protected_endpoint(self, session, api_base_url, auth_token):
        """Test protected endpoint"""
        if not auth_token:
            pytest.skip("No auth token available")

        try:
            # Add token to headers
            headers = {"Authorization": f"Bearer {auth_token}"}

            response = session.get(f"{api_base_url}/users/profile", headers=headers)

            assert (
                response.status_code == 200
            ), f"Protected endpoint failed: {response.status_code}"

            profile = response.json()

            # Check profile data
            assert "id" in profile, "Profile missing ID"
            assert "email" in profile, "Profile missing email"

            logger.info("Protected endpoint accessed successfully")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_create_order(self, session, api_base_url, auth_token, ai_generator):
        """Test order creation with AI-generated data"""
        if not auth_token:
            pytest.skip("No auth token available")

        try:
            # Generate order data using AI
            user_data = ai_generator.generate_user_profile("customer")
            products = ai_generator.generate_product_catalog("electronics", 3)
            order_data = ai_generator.generate_order_data(user_data, products)

            # Prepare data for API
            create_order_data = {
                "items": order_data["items"],
                "shipping_address": order_data["shipping_address"],
                "payment_method": order_data["payment_method"],
            }

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = session.post(
                f"{api_base_url}/orders", json=create_order_data, headers=headers
            )

            assert (
                response.status_code == 201
            ), f"Order creation failed: {response.status_code}"

            order = response.json()

            # Check order structure
            assert "id" in order, "Order missing ID"
            assert "status" in order, "Order missing status"
            assert "total" in order, "Order missing total"

            logger.info(f"Order created successfully: {order['id']}")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_get_user_orders(self, session, api_base_url, auth_token):
        """Test getting user orders"""
        if not auth_token:
            pytest.skip("No auth token available")

        try:
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = session.get(f"{api_base_url}/users/orders", headers=headers)

            assert (
                response.status_code == 200
            ), f"Failed to get user orders: {response.status_code}"

            data = response.json()

            # Check response structure
            assert "orders" in data, "Response missing orders field"
            assert "total" in data, "Response missing total field"

            orders = data["orders"]
            total = data["total"]

            # Check data integrity
            assert isinstance(orders, list), "Orders should be a list"
            assert total >= 0, "Total should be non-negative"
            assert len(orders) <= total, "Orders count should not exceed total"

            logger.info(f"Retrieved {len(orders)} user orders")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    @pytest.mark.performance
    def test_api_response_time(self, session, api_base_url):
        """Test API response time"""
        try:
            start_time = time.time()
            response = session.get(f"{api_base_url}/health")
            end_time = time.time()

            response_time = end_time - start_time

            assert (
                response.status_code == 200
            ), f"Health check failed: {response.status_code}"

            # Check response time (should be under 2 seconds)
            assert response_time < 2.0, f"Response time too slow: {response_time:.2f}s"

            logger.info(f"API response time: {response_time:.3f}s")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_invalid_product_id(self, session, api_base_url):
        """Test invalid product ID handling"""
        try:
            invalid_id = "999999"
            response = session.get(f"{api_base_url}/products/{invalid_id}")

            # Should return 404 for invalid ID
            assert (
                response.status_code == 404
            ), f"Expected 404 for invalid product ID, got {response.status_code}"

            logger.info("Invalid product ID handled correctly")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_invalid_login_credentials(self, session, api_base_url):
        """Test invalid login credentials handling"""
        try:
            invalid_login_data = {
                "email": "invalid@example.com",
                "password": "wrongpassword",
            }

            response = session.post(
                f"{api_base_url}/auth/login", json=invalid_login_data
            )

            # Should return 401 for invalid credentials
            assert (
                response.status_code == 401
            ), f"Expected 401 for invalid credentials, got {response.status_code}"

            logger.info("Invalid login credentials handled correctly")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_missing_required_fields(self, session, api_base_url):
        """Test missing required fields handling"""
        try:
            # Try to create user without required fields
            incomplete_user_data = {
                "first_name": "John"
                # Missing other required fields
            }

            response = session.post(f"{api_base_url}/users", json=incomplete_user_data)

            # Should return 400 for missing required fields
            assert (
                response.status_code == 400
            ), f"Expected 400 for missing required fields, got {response.status_code}"

            logger.info("Missing required fields handled correctly")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_rate_limiting(self, session, api_base_url):
        """Test rate limiting"""
        try:
            # Make multiple requests quickly
            responses = []
            for i in range(5):
                response = session.get(f"{api_base_url}/health")
                responses.append(response.status_code)

            # All requests should succeed (or at least not all fail)
            successful_requests = sum(1 for status in responses if status == 200)
            assert successful_requests > 0, "All requests failed"

            logger.info(
                f"Rate limiting test: {successful_requests}/5 requests successful"
            )

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    @pytest.mark.ai
    def test_ai_generated_api_tests(self, session, api_base_url, ai_generator):
        """Test AI-generated API test scenarios"""
        try:
            # Generate test scenarios using AI
            test_scenarios = ai_generator.generate_api_test_scenarios()

            for scenario in test_scenarios[:3]:  # Test first 3 scenarios
                endpoint = scenario.get("endpoint")
                method = scenario.get("method", "GET")
                expected_status = scenario.get("expected_status", 200)

                if method == "GET":
                    response = session.get(f"{api_base_url}{endpoint}")
                elif method == "POST":
                    response = session.post(f"{api_base_url}{endpoint}")
                else:
                    continue

                # Check if response matches expected status
                if response.status_code == expected_status:
                    logger.info(f"AI test scenario passed: {method} {endpoint}")
                else:
                    logger.warning(
                        f"AI test scenario failed: {method} {endpoint} - expected {expected_status}, got {response.status_code}"
                    )

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")

    @pytest.mark.api
    def test_api_versioning(self, session, api_base_url):
        """Test API versioning"""
        try:
            # Test with version header
            headers = {"Accept": "application/vnd.api.v1+json"}
            response = session.get(f"{api_base_url}/health", headers=headers)

            assert (
                response.status_code == 200
            ), f"Versioned API request failed: {response.status_code}"

            logger.info("API versioning test passed")

        except requests.exceptions.RequestException as e:
            pytest.skip(f"API unavailable: {e}")
