# Mock API Server

This project includes a mock API server for demonstrating API testing capabilities.

## Quick Start

### Option 1: Using the start script
```bash
python start_mock_api.py
```

### Option 2: Direct start
```bash
python mock_api_server.py
```

## Available Endpoints

### Health Check
- **GET** `/health`
- Returns server status and version

### Products
- **GET** `/products` - Get all products
- **GET** `/products/<id>` - Get product by ID
- **GET** `/products/search?q=<query>&limit=<limit>` - Search products

### Users
- **POST** `/users` - Create new user
- **POST** `/auth/login` - User login

### Orders
- **POST** `/orders` - Create new order (requires auth)
- **GET** `/orders` - Get user orders (requires auth)

### API Info
- **GET** `/api/version` - Get API version

## Example Usage

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Products
```bash
curl http://localhost:5000/products
```

### Search Products
```bash
curl "http://localhost:5000/products/search?q=laptop&limit=5"
```

### Create User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

### Create Order (with auth)
```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock_jwt_token_12345" \
  -d '{
    "products": [
      {
        "id": 1,
        "quantity": 2
      }
    ]
  }'
```

## Running Tests with Mock API

1. Start the mock API server:
```bash
python start_mock_api.py
```

2. In another terminal, run API tests:
```bash
source venv/bin/activate
PYTHONPATH=/path/to/project python -m pytest tests/api/ -v
```

## Mock Data

The server includes sample data for:
- 3 products (SmartPhone Pro, Laptop Ultra, Wireless Headphones)
- 1 user (John Doe)
- Empty orders list (populated during testing)

## Features

- ✅ RESTful API endpoints
- ✅ JSON request/response format
- ✅ Error handling (400, 401, 404, 409, 500)
- ✅ Authentication simulation
- ✅ CORS enabled
- ✅ Health check endpoint
- ✅ Search functionality
- ✅ Data validation

## Configuration

The mock API server runs on:
- **Host**: 0.0.0.0 (accessible from any IP)
- **Port**: 5000
- **URL**: http://localhost:5000

## Testing

All API tests in `tests/api/test_api_endpoints.py` are designed to work with this mock server. The tests will now pass instead of failing with 404 errors.
