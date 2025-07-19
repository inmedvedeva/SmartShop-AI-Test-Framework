# How to Run Tests - SmartShop AI Test Framework

## 🚀 Quick Start

### Option 1: Simple Test Runner (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Run simple test runner (bypasses dependency issues)
python run_simple_tests.py
```

### Option 2: Individual Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/home/anonymaus/cursor/SmartShop-AI-Test-Framework

# Run specific tests
python -m pytest tests/api/test_api_endpoints.py::TestAPIEndpoints::test_api_health_check -v
python -m pytest tests/api/test_api_endpoints.py::TestAPIEndpoints::test_get_products -v
python -m pytest tests/api/test_api_endpoints.py::TestAPIEndpoints::test_search_products -v
```

### Option 3: Full Setup Script
```bash
# Run the complete setup script
./quick_start.sh
```

## 📋 Prerequisites

### 1. Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# If you have PostgreSQL issues, remove problematic package
pip uninstall pytest-postgresql -y
```

### 3. Start Mock API Server
```bash
# Start the mock API server (in one terminal)
python start_mock_api.py

# Or use the helper script
python mock_api_server.py
```

## 🧪 Running Different Types of Tests

### API Tests
```bash
# Run all API tests (may have dependency issues)
python -m pytest tests/api/ -v

# Run specific API test
python -m pytest tests/api/test_api_endpoints.py::TestAPIEndpoints::test_api_health_check -v

# Run API tests with markers
python -m pytest -m api -v
```

### UI Tests
```bash
# Run UI tests
python -m pytest tests/ui/ -v

# Run specific UI test
python -m pytest tests/ui/test_automation_exercise_home_page.py -v
```

### Unit Tests
```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run specific unit test
python -m pytest tests/unit/test_ai_data_generator.py -v
```

### Smoke Tests
```bash
# Run smoke tests
python -m pytest -m smoke -v
```

## 🔧 Troubleshooting

### Problem: PostgreSQL Import Error
**Error:** `ImportError: no pq wrapper available`

**Solution:**
```bash
# Remove problematic package
pip uninstall pytest-postgresql -y

# Or install PostgreSQL development libraries
sudo apt-get install libpq-dev  # Ubuntu/Debian
```

### Problem: Pydantic Import Error
**Error:** `ModuleNotFoundError: No module named 'pydantic._internal._signature'`

**Solution:**
```bash
# Update pydantic
pip install --upgrade pydantic pydantic-settings
```

### Problem: Module Import Error
**Error:** `ModuleNotFoundError: No module named 'config.settings'`

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH=/home/anonymaus/cursor/SmartShop-AI-Test-Framework

# Or use the project root
cd /home/anonymaus/cursor/SmartShop-AI-Test-Framework
```

### Problem: Mock API Server Not Running
**Error:** Connection refused to localhost:5000

**Solution:**
```bash
# Start mock API server
python start_mock_api.py

# Check if server is running
curl http://localhost:5000/health
```

## 📊 Expected Test Results

### API Tests (5/5 PASSED)
- ✅ `test_api_health_check` - Health check endpoint
- ✅ `test_get_products` - Get all products
- ✅ `test_search_products` - Search functionality
- ✅ `test_create_user` - User creation
- ✅ `test_user_login` - User authentication

### Test Output Example
```
🚀 SmartShop AI Test Framework - Simple Test Runner
============================================================

📋 Test 1: API Health Check
------------------------------
✅ Health check test PASSED

📋 Test 2: Get Products
------------------------------
✅ Get products test PASSED

📋 Test 3: Search Products
------------------------------
✅ Search products test PASSED

📋 Test 4: Create User
------------------------------
✅ Create user test PASSED

📋 Test 5: User Login
------------------------------
✅ User login test PASSED

============================================================
🎯 Simple Test Runner Complete!
```

## 🎯 Test Categories

### Working Tests (Recommended)
- **API Health Check** - Basic connectivity test
- **Get Products** - Product listing functionality
- **Search Products** - Search functionality
- **Create User** - User registration
- **User Login** - Authentication

### Tests with Known Issues
- **Protected Endpoints** - 404 errors (expected for demo)
- **Order Creation** - Format differences (400 errors)
- **UI Tests** - May fail due to site changes
- **Full Test Suite** - PostgreSQL dependency issues

## 🚀 Quick Commands

### One-Line Test Execution
```bash
# Simple test runner
source venv/bin/activate && python run_simple_tests.py

# Health check only
source venv/bin/activate && PYTHONPATH=/path/to/project python -m pytest tests/api/test_api_endpoints.py::TestAPIEndpoints::test_api_health_check -v

# All working API tests
source venv/bin/activate && PYTHONPATH=/path/to/project python -m pytest tests/api/test_api_endpoints.py::TestAPIEndpoints::test_api_health_check tests/api/test_api_endpoints.py::TestAPIEndpoints::test_get_products tests/api/test_api_endpoints.py::TestAPIEndpoints::test_search_products tests/api/test_api_endpoints.py::TestAPIEndpoints::test_create_user tests/api/test_api_endpoints.py::TestAPIEndpoints::test_user_login -v
```

## 📝 Notes

1. **Mock API Server**: Must be running for API tests to work
2. **Virtual Environment**: Always activate before running tests
3. **PYTHONPATH**: Required for proper module imports
4. **Dependencies**: Some packages may cause conflicts
5. **Demo Purpose**: This is a demonstration project, not production-ready

## 🎉 Success Criteria

Your tests are working correctly if you see:
- ✅ All 5 simple tests pass
- 🟢 Mock API server responds to health check
- 📊 Clean test output without import errors
- 🚀 Tests complete in under 10 seconds
