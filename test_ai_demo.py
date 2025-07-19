#!/usr/bin/env python3
"""
Simple AI Data Generation Demo
Demonstrates how AI generates test data
"""

import json

from utils.ai_data_generator import AIDataGenerator


def main():
    print("🤖 AI Data Generation Demo")
    print("=" * 50)

    # Initialize AI generator
    generator = AIDataGenerator()

    print("\n📝 Generating User Profile...")
    user = generator.generate_user_profile("customer")
    print(f"✅ Generated user: {user['first_name']} {user['last_name']}")
    print(f"   Email: {user['email']}")
    print(f"   City: {user['city']}")
    print(f"   Preferences: {', '.join(user['preferences'])}")

    print("\n🛍️ Generating Product Catalog...")
    products = generator.generate_product_catalog("electronics", 3)
    print(f"✅ Generated {len(products)} products:")
    for i, product in enumerate(products, 1):
        print(f"   {i}. {product['name']} - ${product['price']} ({product['brand']})")

    print("\n📦 Generating Order...")
    order = generator.generate_order_data(user, products)
    print(f"✅ Generated order: {order['order_id']}")
    print(f"   Status: {order['status']}")
    print(f"   Total: ${order['total']}")
    print(f"   Items: {len(order['items'])}")

    print("\n🧪 Generating Test Scenarios...")
    scenarios = generator.generate_test_scenarios("user registration")
    if scenarios:
        print(f"✅ Generated {len(scenarios)} test scenarios")
        for i, scenario in enumerate(scenarios[:2], 1):
            print(f"   {i}. {scenario.get('title', 'Untitled')}")
    else:
        print("⚠️  OpenAI not available, using fallback")

    print("\n📊 Summary:")
    print(f"   • User data: ✅ Generated")
    print(f"   • Product data: ✅ Generated ({len(products)} items)")
    print(f"   • Order data: ✅ Generated")
    print(f"   • Test scenarios: {'✅ Generated' if scenarios else '⚠️ Fallback'}")

    print("\n🎉 AI Data Generation Demo Completed!")


if __name__ == "__main__":
    main()
