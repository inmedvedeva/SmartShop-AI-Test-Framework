"""
Test data management utilities for SmartShop AI Test Framework
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List

from loguru import logger

from src.core.constants import (
    DEFAULT_PRODUCT_CATEGORY,
    DEFAULT_PRODUCT_COUNT,
    DEFAULT_USER_TYPE,
)
from src.core.utils.ai_data_generator import AIDataGenerator


class TestDataManager:
    """Test data management class"""

    def __init__(self, data_dir="resources/test_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.ai_generator = AIDataGenerator()
        self._cached_data = {}

    def load_test_data(self, filename: str) -> dict[str, Any]:
        """Load test data from JSON file"""
        try:
            file_path = self.data_dir / filename
            if file_path.exists():
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"Test data loaded from: {file_path}")
                return data
            else:
                logger.warning(f"Test data file not found: {file_path}")
                return {}

        except Exception as e:
            logger.error(f"Failed to load test data from {filename}: {e}")
            return {}

    def save_test_data(self, filename: str, data: dict[str, Any]) -> bool:
        """Save test data to JSON file"""
        try:
            file_path = self.data_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Test data saved to: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save test data to {filename}: {e}")
            return False

    def generate_user_data(
        self, user_type: str = DEFAULT_USER_TYPE, count: int = 1
    ) -> list[dict[str, Any]]:
        """Generate user test data"""
        try:
            users = []
            for _ in range(count):
                user = self.ai_generator.generate_user_profile(user_type)
                users.append(user)

            logger.info(f"Generated {count} user(s) of type: {user_type}")
            return users

        except Exception as e:
            logger.error(f"Failed to generate user data: {e}")
            return []

    def generate_product_data(
        self,
        category: str = DEFAULT_PRODUCT_CATEGORY,
        count: int = DEFAULT_PRODUCT_COUNT,
    ) -> list[dict[str, Any]]:
        """Generate product test data"""
        try:
            products = []
            for _ in range(count):
                product = self.ai_generator.generate_product_data(category)
                products.append(product)

            logger.info(f"Generated {count} product(s) of category: {category}")
            return products

        except Exception as e:
            logger.error(f"Failed to generate product data: {e}")
            return []

    def get_random_user(self, user_type: str = DEFAULT_USER_TYPE) -> dict[str, Any]:
        """Get a random user from cache or generate new one"""
        cache_key = f"user_{user_type}"

        if cache_key not in self._cached_data:
            self._cached_data[cache_key] = self.generate_user_data(user_type, 10)

        if self._cached_data[cache_key]:
            return random.choice(self._cached_data[cache_key])
        else:
            return {}

    def get_random_product(
        self, category: str = DEFAULT_PRODUCT_CATEGORY
    ) -> dict[str, Any]:
        """Get a random product from cache or generate new one"""
        cache_key = f"product_{category}"

        if cache_key not in self._cached_data:
            self._cached_data[cache_key] = self.generate_product_data(category, 20)

        if self._cached_data[cache_key]:
            return random.choice(self._cached_data[cache_key])
        else:
            return {}

    def create_test_dataset(self, dataset_name: str, data_types: list[str]) -> bool:
        """Create a complete test dataset"""
        try:
            dataset = {
                "name": dataset_name,
                "created_at": str(Path().stat().st_mtime),
                "data": {},
            }

            for data_type in data_types:
                if data_type == "users":
                    dataset["data"]["users"] = self.generate_user_data(count=5)
                elif data_type == "products":
                    dataset["data"]["products"] = self.generate_product_data(count=10)
                elif data_type == "orders":
                    dataset["data"]["orders"] = self.generate_order_data(count=5)

            filename = f"{dataset_name}.json"
            return self.save_test_data(filename, dataset)

        except Exception as e:
            logger.error(f"Failed to create test dataset: {e}")
            return False

    def generate_order_data(self, count: int = 5) -> list[dict[str, Any]]:
        """Generate order test data"""
        try:
            orders = []
            for _ in range(count):
                order = {
                    "order_id": f"ORD-{random.randint(10000, 99999)}",
                    "customer": self.get_random_user(),
                    "products": [
                        self.get_random_product() for _ in range(random.randint(1, 3))
                    ],
                    "total_amount": round(random.uniform(50, 500), 2),
                    "status": random.choice(
                        ["pending", "confirmed", "shipped", "delivered"]
                    ),
                    "payment_method": random.choice(
                        ["credit_card", "paypal", "bank_transfer"]
                    ),
                }
                orders.append(order)

            logger.info(f"Generated {count} order(s)")
            return orders

        except Exception as e:
            logger.error(f"Failed to generate order data: {e}")
            return []

    def clear_cache(self):
        """Clear cached test data"""
        self._cached_data.clear()
        logger.info("Test data cache cleared")


def get_test_data_manager():
    """Factory function to get test data manager"""
    return TestDataManager()
