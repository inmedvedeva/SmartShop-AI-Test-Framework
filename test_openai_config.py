#!/usr/bin/env python3
"""
Test script to check OpenAI configuration
"""

import os

from loguru import logger

from config.settings import settings
from utils.ai_data_generator import AIDataGenerator


def test_openai_config():
    """Test OpenAI configuration"""
    print("🔍 Testing OpenAI Configuration")
    print("=" * 50)

    # Check environment variables
    print("\n1️⃣ Environment Variables:")
    env_key = os.getenv("OPENAI_API_KEY")
    print(f"   OPENAI_API_KEY from env: {'✅ Set' if env_key else '❌ Not set'}")
    if env_key:
        print(f"   Key length: {len(env_key)} characters")
        print(f"   Key starts with: {env_key[:10]}...")

    # Check settings
    print("\n2️⃣ Settings Configuration:")
    print(
        f"   settings.openai_api_key: {'✅ Set' if settings.openai_api_key else '❌ Not set'}"
    )
    if settings.openai_api_key:
        print(f"   Key length: {len(settings.openai_api_key)} characters")
        print(f"   Key starts with: {settings.openai_api_key[:10]}...")

    # Check .env file
    print("\n3️⃣ .env File:")
    try:
        with open(".env") as f:
            env_content = f.read()
        print(f"   .env file exists: ✅")
        print(f"   .env file size: {len(env_content)} bytes")
        if env_content:
            print(f"   .env content: {env_content}")
        else:
            print("   .env file is empty")
    except FileNotFoundError:
        print("   .env file: ❌ Not found")

    # Test AI Data Generator
    print("\n4️⃣ AI Data Generator Test:")
    ai_generator = AIDataGenerator()
    print(
        f"   openai_client: {'✅ Initialized' if ai_generator.openai_client else '❌ Not initialized'}"
    )

    # Test user generation
    print("\n5️⃣ User Generation Test:")
    try:
        user = ai_generator.generate_user_profile("customer")
        print(f"   User generated: ✅")
        print(f"   Method used: {'AI' if ai_generator.openai_client else 'Faker'}")
        print(f"   User name: {user['first_name']} {user['last_name']}")
        print(f"   User email: {user['email']}")
    except Exception as e:
        print(f"   Error generating user: {e}")

    # Test product generation
    print("\n6️⃣ Product Generation Test:")
    try:
        products = ai_generator.generate_product_catalog("electronics", 2)
        print(f"   Products generated: ✅")
        print(f"   Method used: {'AI' if ai_generator.openai_client else 'Faker'}")
        print(f"   Number of products: {len(products)}")
        for i, product in enumerate(products):
            print(f"   Product {i+1}: {product['name']} - ${product['price']}")
    except Exception as e:
        print(f"   Error generating products: {e}")

    print("\n" + "=" * 50)
    print("🎯 Summary:")
    if ai_generator.openai_client:
        print("   ✅ OpenAI is configured and working!")
    else:
        print("   ❌ OpenAI is not configured, using Faker")
        print("   💡 To enable OpenAI, add your API key to .env file:")
        print("      OPENAI_API_KEY=sk-your-key-here")


if __name__ == "__main__":
    test_openai_config()
