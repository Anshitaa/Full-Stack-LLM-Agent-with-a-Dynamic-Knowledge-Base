#!/usr/bin/env python3
"""
Quick test script to verify the setup
"""

import os
import sys
import requests
import time

def test_backend():
    """Test if backend is running and responding"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_frontend():
    """Test if frontend is running and responding"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def main():
    print("🧪 Testing Full-Stack LLM Agent Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = "backend/.env"
    if not os.path.exists(env_file):
        print("⚠️  Environment file not found. Please run:")
        print("   cp backend/env_example.txt backend/.env")
        print("   Then add your OpenAI API key to backend/.env")
        return
    
    # Check if services are running
    print("\n🔍 Checking services...")
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    if backend_ok and frontend_ok:
        print("\n🎉 All services are running successfully!")
        print("\n📱 Access the application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("\n❌ Some services are not running. Please check:")
        print("   1. Run: docker-compose up --build")
        print("   2. Check logs: docker-compose logs")
        print("   3. Ensure OpenAI API key is set in backend/.env")

if __name__ == "__main__":
    main()
