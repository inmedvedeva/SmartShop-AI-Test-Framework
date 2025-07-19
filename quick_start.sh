#!/bin/bash

# Quick Start Script for SmartShop AI Test Framework
# This script sets up and runs the entire project

set -e  # Exit on any error

echo "🚀 SmartShop AI Test Framework - Quick Start"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the SmartShop-AI-Test-Framework directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Check if mock API server is running
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    print_success "Mock API server is already running"
else
    print_status "Starting Mock API server..."
    python start_mock_api.py &
    API_PID=$!

    # Wait for server to start
    print_status "Waiting for API server to start..."
    for i in {1..10}; do
        if curl -s http://localhost:5000/health > /dev/null 2>&1; then
            print_success "Mock API server started successfully"
            break
        fi
        sleep 1
    done

    if [ $i -eq 10 ]; then
        print_error "Failed to start Mock API server"
        exit 1
    fi
fi

# Run API tests
print_status "Running API tests..."
python run_tests.py --markers api

# Show available endpoints
echo ""
echo "📋 Available Mock API Endpoints:"
echo "   GET  http://localhost:5000/health"
echo "   GET  http://localhost:5000/products"
echo "   GET  http://localhost:5000/products/<id>"
echo "   GET  http://localhost:5000/products/search?q=<query>"
echo "   POST http://localhost:5000/users"
echo "   POST http://localhost:5000/auth/login"
echo "   POST http://localhost:5000/orders"
echo "   GET  http://localhost:5000/orders"
echo "   GET  http://localhost:5000/api/version"

echo ""
echo "🎯 Quick Commands:"
echo "   Test API manually: curl http://localhost:5000/health"
echo "   Run all tests: python run_tests.py"
echo "   Run UI tests: python run_tests.py --markers ui"
echo "   Run smoke tests: python run_tests.py --markers smoke"

echo ""
print_success "SmartShop AI Test Framework is ready!"
print_status "Mock API server is running on http://localhost:5000"
print_status "Use Ctrl+C to stop the server when done"

# Keep the script running to keep the API server alive
if [ ! -z "$API_PID" ]; then
    print_status "Press Ctrl+C to stop the Mock API server"
    wait $API_PID
fi
