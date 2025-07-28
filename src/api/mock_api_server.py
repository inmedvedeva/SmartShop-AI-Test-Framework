#!/usr/bin/env python3
"""
Mock API Server for SmartShop AI Test Framework
Demonstrates API testing with a local mock server
"""
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock data
products = [
    {
        "id": 1,
        "name": "SmartPhone Pro",
        "price": 999.99,
        "category": "electronics",
        "description": "Latest smartphone with AI features",
        "stock": 50,
    },
    {
        "id": 2,
        "name": "Laptop Ultra",
        "price": 1499.99,
        "category": "electronics",
        "description": "High-performance laptop for professionals",
        "stock": 25,
    },
    {
        "id": 3,
        "name": "Wireless Headphones",
        "price": 199.99,
        "category": "electronics",
        "description": "Noise-cancelling wireless headphones",
        "stock": 100,
    },
]

users = [
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "address": "123 Main St",
        "city": "New York",
        "country": "USA",
        "postal_code": "10001",
    }
]

orders = []


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {"status": "ok", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}
    )


@app.route("/products", methods=["GET"])
def get_products():
    """Get all products"""
    return jsonify({"products": products, "total": len(products)})


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get product by ID"""
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


@app.route("/products/search", methods=["GET"])
def search_products():
    """Search products"""
    query = request.args.get("q", "").lower()
    limit = int(request.args.get("limit", 10))

    filtered_products = [
        p
        for p in products
        if query in p["name"].lower() or query in p["description"].lower()
    ]

    return jsonify(
        {
            "products": filtered_products[:limit],
            "total": len(filtered_products),
            "query": query,
        }
    )


@app.route("/users", methods=["POST"])
def create_user():
    """Create new user"""
    data = request.get_json()

    # Validate required fields
    required_fields = ["first_name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Check if email already exists
    if any(u["email"] == data["email"] for u in users):
        return jsonify({"error": "Email already exists"}), 409

    # Create new user
    new_user = {
        "id": len(users) + 1,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "phone": data.get("phone", ""),
        "address": data.get("address", ""),
        "city": data.get("city", ""),
        "country": data.get("country", ""),
        "postal_code": data.get("postal_code", ""),
    }

    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/auth/login", methods=["POST"])
def login():
    """User login"""
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    # Mock authentication - accept any valid email format
    if "@" in data["email"] and len(data["password"]) >= 6:
        return jsonify(
            {
                "token": "mock_jwt_token_12345",
                "user": {"email": data["email"], "role": "customer"},
            }
        )

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/orders", methods=["POST"])
def create_order():
    """Create new order"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization required"}), 401

    data = request.get_json()

    if not data or "products" not in data:
        return jsonify({"error": "Products required"}), 400

    # Create order
    new_order = {
        "id": len(orders) + 1,
        "user_id": 1,  # Mock user ID
        "products": data["products"],
        "total": sum(
            p.get("price", 0) * p.get("quantity", 1) for p in data["products"]
        ),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    orders.append(new_order)
    return jsonify(new_order), 201


@app.route("/orders", methods=["GET"])
def get_user_orders():
    """Get user orders"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization required"}), 401

    return jsonify({"orders": orders, "total": len(orders)})


@app.route("/api/version", methods=["GET"])
def api_version():
    """API version endpoint"""
    return jsonify({"version": "1.0.0", "status": "stable", "documentation": "/docs"})


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("🚀 Starting Mock API Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📋 Available endpoints:")
    print("   GET  /health")
    print("   GET  /products")
    print("   GET  /products/<id>")
    print("   GET  /products/search?q=<query>")
    print("   POST /users")
    print("   POST /auth/login")
    print("   POST /orders")
    print("   GET  /orders")
    print("   GET  /api/version")
    print("\n💡 Use Ctrl+C to stop the server")

    app.run(host="0.0.0.0", port=5000, debug=True)
