#!/usr/bin/env python3
"""
Script to create a test user for V2T system
"""
import requests
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.user import OTPCode

BASE_URL = "http://localhost:8000"

# Test user credentials
test_user = {
    "name": "Test User",
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "TestPassword123!",
    "role": "Student"
}

def main():
    print("=" * 60)
    print("Creating Test User for V2T System")
    print("=" * 60)

    # Step 1: Signup
    print("\n[1/3] Creating user account...")
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=test_user)
        if response.status_code == 200:
            print("✓ User created successfully!")
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            if "already registered" in error_detail.lower():
                print("⚠ User already exists")
            else:
                print(f"✗ Error: {error_detail}")
                return
    except Exception as e:
        print(f"✗ Error: {e}")
        return

    # Step 2: Get OTP from database
    print("\n[2/3] Fetching OTP code from database...")
    try:
        db = SessionLocal()
        otp_record = db.query(OTPCode).filter(
            OTPCode.email == test_user['email'],
            OTPCode.is_used == False
        ).order_by(OTPCode.created_at.desc()).first()

        if otp_record:
            otp_code = otp_record.code
            print(f"✓ OTP Code retrieved: {otp_code}")
            
            # Step 3: Verify OTP
            print("\n[3/3] Verifying OTP...")
            verify_response = requests.post(
                f"{BASE_URL}/auth/verify-otp",
                json={"email": test_user['email'], "otp": otp_code}
            )
            
            if verify_response.status_code == 200:
                print("✓ Email verified successfully!")
            else:
                print(f"✗ Verification failed: {verify_response.json().get('detail', 'Unknown error')}")
        else:
            print("⚠ No OTP found (user may already be verified)")
        
        db.close()
    except Exception as e:
        print(f"✗ Error: {e}")
        return

    # Display credentials
    print("\n" + "=" * 60)
    print("TEST USER CREDENTIALS")
    print("=" * 60)
    print(f"Name:     {test_user['name']}")
    print(f"Username: {test_user['username']}")
    print(f"Email:    {test_user['email']}")
    print(f"Password: {test_user['password']}")
    print(f"Role:     {test_user['role']}")
    print("=" * 60)
    print("\n✓ You can now login with these credentials!")
    print(f"\nFrontend: http://localhost:3001")
    print(f"Backend:  http://localhost:8000/docs")
    print("=" * 60)

if __name__ == "__main__":
    main()
