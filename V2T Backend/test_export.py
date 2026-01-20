#!/usr/bin/env python3
"""
Test script for PDF and Text export functionality
"""

import requests
import sys
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_export_endpoints():
    """Test the export functionality"""
    
    print("=" * 70)
    print("  V2T Backend - Export Feature Test")
    print("=" * 70)
    print()
    
    # Step 1: Check server
    print("1. Checking server status...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print("   ✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running. Start with: ./start_servers.sh")
        return False
    
    # Step 2: Login
    print("\n2. Testing authentication...")
    username = input("   Enter username: ").strip()
    password = input("   Enter password: ").strip()
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username_or_email": username, "password": password}
        )
        
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.json().get('detail')}")
            return False
        
        token = response.json()["access_token"]
        print("   ✅ Authentication successful")
        
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: List videos
    print("\n3. Fetching available videos...")
    try:
        response = requests.get(f"{BASE_URL}/video/list", headers=headers)
        videos = response.json().get("videos", [])
        
        if not videos:
            print("   ⚠️  No videos found. Upload a video first.")
            return False
        
        print(f"   ✅ Found {len(videos)} video(s)")
        
        # Show completed videos
        completed_videos = [v for v in videos if v["status"] == "completed"]
        
        if not completed_videos:
            print("   ⚠️  No completed videos available for export")
            print("\n   Available videos:")
            for idx, video in enumerate(videos, 1):
                print(f"     {idx}. {video['filename']} - Status: {video['status']}")
            return False
        
        print("\n   Completed videos available for export:")
        for idx, video in enumerate(completed_videos, 1):
            print(f"     {idx}. {video['filename']} (ID: {video['video_id']})")
        
    except Exception as e:
        print(f"   ❌ Error fetching videos: {e}")
        return False
    
    # Step 4: Select video
    print("\n4. Select video to export:")
    try:
        selection = int(input(f"   Enter number (1-{len(completed_videos)}): "))
        if selection < 1 or selection > len(completed_videos):
            print("   ❌ Invalid selection")
            return False
        
        selected_video = completed_videos[selection - 1]
        video_id = selected_video["video_id"]
        print(f"   ✅ Selected: {selected_video['filename']}")
        
    except ValueError:
        print("   ❌ Invalid input")
        return False
    
    # Step 5: Export to Text
    print(f"\n5. Exporting to Text file...")
    try:
        response = requests.get(
            f"{BASE_URL}/video/export/{video_id}/text",
            headers=headers
        )
        
        if response.status_code == 200:
            # Save file
            filename = f"export_test_{video_id}.txt"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = Path(filename).stat().st_size
            print(f"   ✅ Text file downloaded: {filename} ({file_size:,} bytes)")
            
            # Show preview
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print("\n   Preview (first 10 lines):")
                for line in lines[:10]:
                    print(f"     {line.rstrip()}")
        else:
            print(f"   ❌ Export failed: {response.json().get('detail')}")
            
    except Exception as e:
        print(f"   ❌ Error exporting text: {e}")
    
    # Step 6: Export to PDF
    print(f"\n6. Exporting to PDF file...")
    try:
        response = requests.get(
            f"{BASE_URL}/video/export/{video_id}/pdf",
            headers=headers
        )
        
        if response.status_code == 200:
            # Save file
            filename = f"export_test_{video_id}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = Path(filename).stat().st_size
            print(f"   ✅ PDF file downloaded: {filename} ({file_size:,} bytes)")
            print(f"   📄 Open the PDF to view formatted results")
        else:
            print(f"   ❌ Export failed: {response.json().get('detail')}")
            
    except Exception as e:
        print(f"   ❌ Error exporting PDF: {e}")
    
    print("\n" + "=" * 70)
    print("  Export Test Complete!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        test_export_endpoints()
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
