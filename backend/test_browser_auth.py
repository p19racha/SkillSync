#!/usr/bin/env python3
"""
Test script to verify the complete profile edit workflow with browser debugging
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5001"

def test_auth_flow():
    """Test the authentication flow that the browser would go through"""
    print("=== Testing Browser Authentication Flow ===\n")
    
    # Create a session to maintain cookies like a browser
    session = requests.Session()
    
    # Test 1: Check auth status (should be false)
    print("1. Testing initial auth status...")
    auth_response = session.get(f"{BASE_URL}/api/check-auth")
    print(f"   Status: {auth_response.status_code}")
    auth_data = auth_response.json()
    print(f"   Response: {auth_data}")
    
    if auth_data.get('authenticated'):
        print("   ❌ User is already authenticated - need to logout first")
        return
    
    print("   ✅ User is not authenticated (as expected)")
    
    # Test 2: Try to access profile without auth (should fail)
    print("\n2. Testing profile access without auth...")
    profile_response = session.get(f"{BASE_URL}/api/complete-profile")
    print(f"   Status: {profile_response.status_code}")
    
    if profile_response.status_code == 401:
        print("   ✅ Profile access blocked without auth (as expected)")
    else:
        print(f"   ❌ Unexpected response: {profile_response.text}")
    
    # Test 3: Login with test credentials
    print("\n3. Testing login...")
    login_data = {
        "username": "test_user_edit",
        "password": "test123"
    }
    
    login_response = session.post(
        f"{BASE_URL}/login",
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"   Status: {login_response.status_code}")
    if login_response.status_code in [200, 201]:
        login_result = login_response.json()
        print(f"   Response: {login_result}")
        print("   ✅ Login successful")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    # Test 4: Check auth status after login
    print("\n4. Testing auth status after login...")
    auth_response = session.get(f"{BASE_URL}/api/check-auth")
    print(f"   Status: {auth_response.status_code}")
    auth_data = auth_response.json()
    print(f"   Response: {auth_data}")
    
    if auth_data.get('authenticated'):
        print("   ✅ User is now authenticated")
    else:
        print("   ❌ User is still not authenticated")
        return
    
    # Test 5: Access profile after auth
    print("\n5. Testing profile access after auth...")
    profile_response = session.get(f"{BASE_URL}/api/complete-profile")
    print(f"   Status: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"   Response: {profile_data}")
        print("   ✅ Profile accessed successfully")
        
        if profile_data.get('success') and profile_data.get('profile'):
            print("   ✅ Profile data exists - this should trigger EDIT mode")
        else:
            print("   ⚠️  No profile data - this should trigger CREATE mode")
    
    elif profile_response.status_code == 404:
        print("   ⚠️  No profile found - this should trigger CREATE mode")
    else:
        print(f"   ❌ Unexpected response: {profile_response.text}")
    
    print("\n=== Browser Authentication Flow Test Complete ===")
    print("\nTo debug frontend issues:")
    print("1. Check browser console for debug output")
    print("2. Verify the page can login before accessing profile")
    print("3. Check if JavaScript is loading the CompleteProfilePage class")

if __name__ == "__main__":
    test_auth_flow()