#!/usr/bin/env python3
"""
Test script for V2T Backend Video Processing API
"""

import requests
import time
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_json(data):
    print(json.dumps(data, indent=2))

def test_signup(name, username, email, password, role="Student"):
    """Test user signup"""
    print_header("Testing Signup")
    
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "name": name,
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
    )
    
    print(f"Status: {response.status_code}")
    print_json(response.json())
    
    return response.status_code == 201

def test_verify_otp(email, otp):
    """Test OTP verification"""
    print_header("Testing OTP Verification")
    
    response = requests.post(
        f"{BASE_URL}/auth/verify-otp",
        json={
            "email": email,
            "otp": otp
        }
    )
    
    print(f"Status: {response.status_code}")
    print_json(response.json())
    
    return response.status_code == 200

def test_login(username, password):
    """Test user login"""
    print_header("Testing Login")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username_or_email": username,
            "password": password
        }
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print_json(data)
    
    if response.status_code == 200:
        return data.get("access_token")
    return None

def test_video_upload(token, video_path):
    """Test video upload"""
    print_header("Testing Video Upload")
    
    if not Path(video_path).exists():
        print(f"❌ Video file not found: {video_path}")
        return None
    
    with open(video_path, 'rb') as f:
        files = {'file': (Path(video_path).name, f, 'video/mp4')}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/video/upload",
            files=files,
            headers=headers
        )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print_json(data)
    
    if response.status_code == 200:
        return data.get("video_id")
    return None

def test_video_status(token, video_id):
    """Test video status check"""
    print_header(f"Testing Video Status (ID: {video_id})")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f"{BASE_URL}/video/status/{video_id}",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print_json(data)
    
    return data.get("status")

def test_video_results(token, video_id):
    """Test video results retrieval"""
    print_header(f"Testing Video Results (ID: {video_id})")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f"{BASE_URL}/video/results/{video_id}",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print_json(data)
    
    return response.status_code == 200

def test_video_list(token):
    """Test list all videos"""
    print_header("Testing Video List")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f"{BASE_URL}/video/list",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print_json(response.json())
    
    return response.status_code == 200

def wait_for_processing(token, video_id, max_wait=120):
    """Wait for video processing to complete"""
    print_header("Waiting for Video Processing")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        status = test_video_status(token, video_id)
        
        if status == "completed":
            print("\n✅ Video processing completed!")
            return True
        elif status == "failed":
            print("\n❌ Video processing failed!")
            return False
        
        print(f"\nStatus: {status} - Waiting 5 seconds...")
        time.sleep(5)
    
    print(f"\n⏰ Timeout after {max_wait} seconds")
    return False

def main():
    print_header("V2T Backend API Test Suite")
    
    # Configuration
    test_user = {
        "name": "Test User",
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "TestPassword123!",
        "role": "Student"
    }
    
    # Test 1: Check if server is running
    print_header("Checking Server Status")
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Server is running")
        print_json(response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("Start the server with: ./start_servers.sh")
        sys.exit(1)
    
    # Test 2: Signup
    if not test_signup(**test_user):
        print("❌ Signup failed!")
        sys.exit(1)
    
    # Test 3: Get OTP from console (in production it would be from email)
    print_header("OTP Verification Required")
    print("\n⚠️  Check the server console for the OTP")
    print("In production, the OTP would be sent to email")
    otp = input("\nEnter OTP (or press Enter to skip): ").strip()
    
    if otp:
        test_verify_otp(test_user["email"], otp)
    else:
        print("Skipping OTP verification...")
    
    # Test 4: Login
    token = test_login(test_user["username"], test_user["password"])
    if not token:
        print("❌ Login failed!")
        sys.exit(1)
    
    print(f"\n✅ Authentication successful!")
    print(f"Token: {token[:50]}...")
    
    # Test 5: Video Upload
    print_header("Video Upload Test")
    video_path = input("\nEnter path to test video file (or press Enter to skip): ").strip()
    
    if not video_path:
        print("Skipping video upload test...")
        print("\n" + "="*60)
        print("  Test Complete - Authentication Tests Passed!")
        print("="*60)
        return
    
    video_id = test_video_upload(token, video_path)
    if not video_id:
        print("❌ Video upload failed!")
        return
    
    # Test 6: Wait for processing
    if wait_for_processing(token, video_id):
        # Test 7: Get results
        test_video_results(token, video_id)
    
    # Test 8: List videos
    test_video_list(token)
    
    print_header("All Tests Completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
