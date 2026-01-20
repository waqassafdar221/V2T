"""
Test script for authentication endpoints.

Usage:
    python test_auth.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup."""
    print("\n" + "="*60)
    print("Testing User Signup")
    print("="*60)
    
    data = {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "role": "Student",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()


def test_verify_otp(email, otp):
    """Test OTP verification."""
    print("\n" + "="*60)
    print("Testing OTP Verification")
    print("="*60)
    
    data = {
        "email": email,
        "otp": otp
    }
    
    response = requests.post(f"{BASE_URL}/auth/verify-otp", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()


def test_login(username_or_email, password):
    """Test user login."""
    print("\n" + "="*60)
    print("Testing User Login")
    print("="*60)
    
    data = {
        "username_or_email": username_or_email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()


def test_health_check():
    """Test health check endpoint."""
    print("\n" + "="*60)
    print("Testing Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("\n🚀 V2T Backend Authentication Test Suite")
    print("="*60)
    
    # Test health check
    test_health_check()
    
    # Test signup
    signup_result = test_signup()
    
    print("\n" + "="*60)
    print("⚠️  CHECK YOUR TERMINAL OUTPUT FOR OTP CODE")
    print("="*60)
    
    # Prompt for OTP
    otp = input("\nEnter the OTP from terminal output: ")
    
    # Test OTP verification
    test_verify_otp("test@example.com", otp)
    
    # Test login
    test_login("testuser", "password123")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
