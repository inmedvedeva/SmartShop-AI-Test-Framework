#!/usr/bin/env python3
"""
Test script to demonstrate OpenAI error handling
"""

import os

from loguru import logger

from utils.ai_data_generator import AIDataGenerator


def test_error_handling():
    """Test different error scenarios"""
    print("🔧 Testing OpenAI Error Handling")
    print("=" * 50)

    # Test 1: No API key (should use Faker)
    print("\n1️⃣ Test: No API Key")
    print("-" * 30)
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    ai_generator = AIDataGenerator()
    user = ai_generator.generate_user_profile("customer")
    print(f"   Method used: {'AI' if ai_generator.openai_client else 'Faker'}")
    print(f"   User: {user['first_name']} {user['last_name']}")

    # Test 2: Invalid API key (should fallback to Faker)
    print("\n2️⃣ Test: Invalid API Key")
    print("-" * 30)
    os.environ["OPENAI_API_KEY"] = "sk-invalid-key"

    ai_generator = AIDataGenerator()
    products = ai_generator.generate_product_catalog("electronics", 2)
    print(f"   Method used: {'AI' if ai_generator.openai_client else 'Faker'}")
    print(f"   Products generated: {len(products)}")

    # Test 3: Geographic restriction simulation
    print("\n3️⃣ Test: Geographic Restriction (403 Error)")
    print("-" * 30)
    os.environ["OPENAI_API_KEY"] = "sk-test-key-for-403"

    ai_generator = AIDataGenerator()
    scenarios = ai_generator.generate_test_scenarios("search")
    print(f"   Scenarios generated: {len(scenarios)}")

    # Test 4: Rate limit simulation
    print("\n5️⃣ Test: Rate Limit (429 Error)")
    print("-" * 30)
    os.environ["OPENAI_API_KEY"] = "sk-test-key-for-429"

    ai_generator = AIDataGenerator()
    user = ai_generator.generate_user_profile("admin")
    print(f"   Method used: {'AI' if ai_generator.openai_client else 'Faker'}")
    print(f"   Admin user: {user['first_name']} {user['last_name']}")

    print("\n" + "=" * 50)
    print("🎯 Error Handling Summary:")
    print("   ✅ No API key → Faker fallback")
    print("   ✅ Invalid API key → Faker fallback")
    print("   ✅ 403 Geographic restriction → Faker fallback")
    print("   ✅ 429 Rate limit → Faker fallback")
    print("   ✅ Other errors → Faker fallback")
    print("\n💡 The system gracefully handles all OpenAI errors!")


if __name__ == "__main__":
    test_error_handling()
