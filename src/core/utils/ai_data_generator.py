"""
AI-powered test data generator
Uses OpenAI to create realistic test data
"""

import json
import random
from typing import Any

import openai
from faker import Faker
from loguru import logger

from src.core.config.settings import settings


class AIDataGenerator:
    """Test data generator using AI"""

    def __init__(self):
        self.fake = Faker(["en_US"])
        self.openai_client = None

        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
            self.openai_client = openai.OpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OpenAI API key not configured, will use Faker")

    def generate_user_profile(self, user_type: str = "customer") -> dict[str, Any]:
        """
        Generates user profile using AI

        Args:
            user_type: User type (customer, admin, vendor)

        Returns:
            Dict with user data
        """
        if self.openai_client:
            return self._generate_user_with_ai(user_type)
        else:
            return self._generate_user_with_faker(user_type)

    def _generate_user_with_ai(self, user_type: str) -> dict[str, Any]:
        """Generate user using OpenAI"""
        try:
            prompt = f"""
            Generate a realistic user profile for an e-commerce website.
            User type: {user_type}

            Return JSON with fields:
            - first_name: first name
            - last_name: last name
            - email: email
            - phone: phone number
            - address: address
            - city: city
            - country: country
            - postal_code: postal code
            - date_of_birth: date of birth (YYYY-MM-DD)
            - preferences: list of shopping preferences
            - loyalty_points: loyalty points
            - registration_date: registration date (YYYY-MM-DD)

            Make data realistic for {user_type} user.
            """

            response = self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )

            content = response.choices[0].message.content
            # Extract JSON from response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            json_str = content[json_start:json_end]

            user_data = json.loads(json_str)
            logger.info(f"Generated {user_type} user with AI")
            return user_data

        except Exception as e:
            error_msg = str(e)
            if (
                "403" in error_msg
                and "unsupported_country_region_territory" in error_msg
            ):
                logger.warning(
                    f"OpenAI blocked due to geographic restrictions, falling back to Faker for {user_type} user"
                )
            elif "401" in error_msg and "invalid_api_key" in error_msg:
                logger.warning(
                    f"Invalid OpenAI API key, falling back to Faker for {user_type} user"
                )
            elif "429" in error_msg:
                logger.warning(
                    f"OpenAI rate limit exceeded, falling back to Faker for {user_type} user"
                )
            else:
                logger.error(f"AI generation error for {user_type} user: {e}")

            return self._generate_user_with_faker(user_type)

    def _generate_user_with_faker(self, user_type: str) -> dict[str, Any]:
        """Generate user using Faker"""
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "address": self.fake.street_address(),
            "city": self.fake.city(),
            "country": self.fake.country(),
            "postal_code": self.fake.postcode(),
            "date_of_birth": self.fake.date_of_birth(
                minimum_age=18, maximum_age=80
            ).strftime("%Y-%m-%d"),
            "preferences": self._generate_preferences(user_type),
            "loyalty_points": random.randint(0, 10000),
            "registration_date": self.fake.date_between(
                start_date="-2y", end_date="today"
            ).strftime("%Y-%m-%d"),
        }

        logger.info(f"Generated {user_type} user with Faker")
        return user_data

    def generate_product_catalog(
        self, category: str = "electronics", count: int = 10
    ) -> list[dict[str, Any]]:
        """
        Generates product catalog

        Args:
            category: Product category
            count: Number of products

        Returns:
            List with product data
        """
        if self.openai_client:
            return self._generate_products_with_ai(category, count)
        else:
            return self._generate_products_with_faker(category, count)

    def _generate_products_with_ai(
        self, category: str, count: int
    ) -> list[dict[str, Any]]:
        """Generate products using OpenAI"""
        try:
            prompt = f"""
            Generate {count} realistic products for category "{category}".

            Return JSON array with objects containing fields:
            - name: product name
            - description: description
            - price: price (number)
            - currency: currency
            - category: category
            - brand: brand
            - sku: SKU
            - stock_quantity: stock quantity
            - rating: rating (0-5)
            - features: array of features
            - images: array of image URLs

            Make data realistic for category {category}.
            """

            response = self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )

            content = response.choices[0].message.content
            json_start = content.find("[")
            json_end = content.rfind("]") + 1
            json_str = content[json_start:json_end]

            products = json.loads(json_str)
            logger.info(
                f"Generated {len(products)} products in category {category} with AI"
            )
            return products

        except Exception as e:
            error_msg = str(e)
            if (
                "403" in error_msg
                and "unsupported_country_region_territory" in error_msg
            ):
                logger.warning(
                    f"OpenAI blocked due to geographic restrictions, falling back to Faker for {category} products"
                )
            elif "401" in error_msg and "invalid_api_key" in error_msg:
                logger.warning(
                    f"Invalid OpenAI API key, falling back to Faker for {category} products"
                )
            elif "429" in error_msg:
                logger.warning(
                    f"OpenAI rate limit exceeded, falling back to Faker for {category} products"
                )
            else:
                logger.error(f"Error generating products with AI for {category}: {e}")

            return self._generate_products_with_faker(category, count)

    def _generate_products_with_faker(
        self, category: str, count: int
    ) -> list[dict[str, Any]]:
        """Generate products using Faker"""
        products = []

        for i in range(count):
            product = {
                "name": self._generate_product_name(category),
                "description": self.fake.text(max_nb_chars=200),
                "price": round(random.uniform(10, 2000), 2),
                "currency": "USD",
                "category": category,
                "brand": self._generate_brand(category),
                "sku": f"{category.upper()}{random.randint(1000, 9999)}",
                "stock_quantity": random.randint(0, 100),
                "rating": round(random.uniform(1, 5), 1),
                "features": self._generate_features(category),
                "images": [f"https://example.com/images/{category}/{i+1}.jpg"],
            }
            products.append(product)

        logger.info(
            f"Generated {len(products)} products in category {category} with Faker"
        )
        return products

    def generate_order_data(
        self, user_data: dict[str, Any], products: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Generates order data

        Args:
            user_data: User data
            products: Product list

        Returns:
            Dict with order data
        """
        selected_products = random.sample(products, min(3, len(products)))
        order_items = []
        total_amount = 0

        for product in selected_products:
            quantity = random.randint(1, 3)
            item_total = product["price"] * quantity
            total_amount += item_total

            order_items.append(
                {
                    "product_id": product["sku"],
                    "product_name": product["name"],
                    "quantity": quantity,
                    "unit_price": product["price"],
                    "total_price": item_total,
                }
            )

        order_data = {
            "order_id": f"ORD{random.randint(100000, 999999)}",
            "user_id": user_data.get("email"),
            "order_date": self.fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
            "status": random.choice(["pending", "confirmed", "shipped", "delivered"]),
            "items": order_items,
            "subtotal": total_amount,
            "tax": round(total_amount * 0.1, 2),
            "shipping": round(random.uniform(5, 20), 2),
            "total": round(total_amount * 1.1 + random.uniform(5, 20), 2),
            "shipping_address": {
                "street": user_data["address"],
                "city": user_data["city"],
                "country": user_data["country"],
                "postal_code": user_data["postal_code"],
            },
            "payment_method": random.choice(["credit_card", "paypal", "bank_transfer"]),
        }

        logger.info(f"Generated order {order_data['order_id']}")
        return order_data

    def _generate_preferences(self, user_type: str) -> list[str]:
        """Generate user preferences"""
        all_preferences = [
            "electronics",
            "clothing",
            "books",
            "sports",
            "home",
            "beauty",
            "automotive",
            "toys",
            "garden",
            "health",
            "food",
            "jewelry",
        ]

        if user_type == "admin":
            return ["management", "analytics", "reports"]
        elif user_type == "vendor":
            return ["inventory", "sales", "marketing"]
        else:
            return random.sample(all_preferences, random.randint(2, 5))

    def _generate_product_name(self, category: str) -> str:
        """Generate product name"""
        category_names = {
            "electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Camera"],
            "clothing": ["T-Shirt", "Jeans", "Dress", "Shoes", "Jacket"],
            "books": ["Novel", "Textbook", "Magazine", "Comic", "Guide"],
            "sports": ["Ball", "Racket", "Bike", "Treadmill", "Weights"],
        }

        names = category_names.get(category, ["Product"])
        return f"{random.choice(names)} {self.fake.word().title()}"

    def _generate_brand(self, category: str) -> str:
        """Generate brand"""
        category_brands = {
            "electronics": ["Apple", "Samsung", "Sony", "LG", "Dell"],
            "clothing": ["Nike", "Adidas", "Zara", "H&M", "Uniqlo"],
            "books": ["Penguin", "Random House", "HarperCollins", "Simon & Schuster"],
            "sports": ["Nike", "Adidas", "Under Armour", "Puma", "Reebok"],
        }

        brands = category_brands.get(category, ["Generic"])
        return random.choice(brands)

    def _generate_features(self, category: str) -> list[str]:
        """Generate product features"""
        category_features = {
            "electronics": ["Wireless", "Bluetooth", "HD", "4K", "Fast Charging"],
            "clothing": ["Cotton", "Polyester", "Waterproof", "Breathable", "Stretch"],
            "books": ["Hardcover", "Paperback", "Digital", "Illustrated", "Signed"],
            "sports": [
                "Lightweight",
                "Durable",
                "Adjustable",
                "Anti-slip",
                "Waterproof",
            ],
        }

        features = category_features.get(category, ["Quality", "Reliable"])
        # Ensure we don't try to sample more features than available
        sample_size = min(random.randint(2, 4), len(features))
        return random.sample(features, sample_size)

    def generate_search_terms(self, count: int = 5) -> list[str]:
        """
        Generate search terms for testing

        Args:
            count: Number of search terms to generate

        Returns:
            List of search terms
        """
        search_terms = [
            "dress",
            "shirt",
            "jeans",
            "shoes",
            "bag",
            "watch",
            "phone",
            "laptop",
            "book",
            "toy",
            "food",
            "drink",
            "car",
            "bike",
            "house",
            "garden",
            "beauty",
            "health",
            "sports",
            "music",
            "art",
            "tech",
            "fashion",
        ]

        return random.sample(search_terms, min(count, len(search_terms)))

    def generate_test_scenarios(self, feature: str) -> list[dict[str, Any]]:
        """
        Generate test scenarios using AI

        Args:
            feature: Functionality to test

        Returns:
            List with test scenarios
        """
        if not self.openai_client:
            logger.warning("OpenAI not available for scenario generation")
            return []

        try:
            prompt = f"""
            Generate 5 test scenarios for feature "{feature}" e-commerce website.

            Return JSON array with objects containing:
            - title: scenario title
            - description: description
            - steps: array of steps
            - expected_result: expected result
            - priority: priority (high/medium/low)
            - tags: array of tags

            Make scenarios diverse: positive, negative, edge cases.
            """

            response = self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )

            content = response.choices[0].message.content
            json_start = content.find("[")
            json_end = content.rfind("]") + 1
            json_str = content[json_start:json_end]

            scenarios = json.loads(json_str)
            logger.info(f"Generated {len(scenarios)} scenarios for feature {feature}")
            return scenarios

        except Exception as e:
            error_msg = str(e)
            if (
                "403" in error_msg
                and "unsupported_country_region_territory" in error_msg
            ):
                logger.warning(
                    f"OpenAI blocked due to geographic restrictions for {feature} scenarios"
                )
            elif "401" in error_msg and "invalid_api_key" in error_msg:
                logger.warning(f"Invalid OpenAI API key for {feature} scenarios")
            elif "429" in error_msg:
                logger.warning(f"OpenAI rate limit exceeded for {feature} scenarios")
            else:
                logger.error(f"Error generating scenarios for {feature}: {e}")

            return []
