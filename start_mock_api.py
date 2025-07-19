#!/usr/bin/env python3
"""
Script to start the Mock API Server for testing
"""
import subprocess
import sys
import time
from pathlib import Path

import requests


def install_requirements():
    """Install required packages"""
    print("📦 Installing Flask requirements...")
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "flask==3.0.0",
                "flask-cors==4.0.0",
            ],
            check=True,
            capture_output=True,
        )
        print("✅ Flask requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Flask requirements: {e}")
        return False
    return True


def check_server_health():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def start_mock_api():
    """Start the mock API server"""
    print("🚀 Starting Mock API Server...")

    # Install requirements if needed
    if not install_requirements():
        return False

    # Start the server
    try:
        server_process = subprocess.Popen(
            [sys.executable, "mock_api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(10):
            if check_server_health():
                print("✅ Mock API Server is running at http://localhost:5000")
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
                print("\n💡 Press Ctrl+C to stop the server")

                # Keep the server running
                try:
                    server_process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping Mock API Server...")
                    server_process.terminate()
                    server_process.wait()
                    print("✅ Server stopped")

                return True

            time.sleep(1)

        print("❌ Server failed to start within 10 seconds")
        server_process.terminate()
        return False

    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False


if __name__ == "__main__":
    start_mock_api()
