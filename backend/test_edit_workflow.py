#!/usr/bin/env python3
"""
Test script to verify the complete profile edit functionality
"""

import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:5001"

def test_edit_profile_workflow():
    """Test the complete edit profile workflow"""
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("=== Testing Edit Profile Workflow ===")
    
    # Step 1: Register/Login a test user
    print("\n1. Testing user authentication...")
    
    # Try to login first
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = session.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code != 200:
        # If login fails, try to register
        print("Login failed, attempting registration...")
        register_data = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "testpass123"
        }
        
        response = session.post(f"{BASE_URL}/register", json=register_data)
        print(f"Register response: {response.status_code}")
        
        if response.status_code in [200, 201]:
            # Now login
            response = session.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code not in [200, 201]:
        print(f"❌ Authentication failed: {response.status_code} - {response.text}")
        return False
    
    print(f"✅ Authentication successful: {response.json()}")
    
    # Step 2: Check if profile exists (should return 404 initially)
    print("\n2. Checking for existing profile...")
    response = session.get(f"{BASE_URL}/api/complete-profile")
    print(f"Get profile response: {response.status_code}")
    
    if response.status_code == 404:
        print("✅ No existing profile found (expected for new user)")
        has_existing_profile = False
    elif response.status_code == 200:
        print("✅ Found existing profile")
        profile_data = response.json()
        print(f"Existing profile: {json.dumps(profile_data, indent=2)}")
        has_existing_profile = True
    else:
        print(f"❌ Unexpected response: {response.status_code} - {response.text}")
        return False
    
    # Step 3: Create profile if doesn't exist
    if not has_existing_profile:
        print("\n3. Creating new profile...")
        profile_data = {
            "aadhar_id": "987654321098",  # Different Aadhar ID to avoid duplicates
            "name": "Test User",
            "dob": "1995-06-15",
            "state": "Karnataka",
            "city": "Bangalore",
            "pincode": "560001",
            "education_level": "Undergraduate",
            "degree": "B.Tech Computer Science",
            "year_of_study": "3rd Year",
            "gpa_percentage": 8.5,
            "relevant_courses": "Data Structures, Algorithms",
            "technical_skills": "Python, JavaScript",
            "soft_skills": "Communication, Leadership",
            "previous_internships": "Summer intern at Tech Corp",
            "projects": "E-commerce website",
            "hackathons_competitions": "College hackathon winner",
            "research_experience": "AI research project",
            "internship_type_preference": "Hybrid",
            "duration_preference": "3-6 months",
            "stipend_expectation": "10k-25k",
            "preferred_industry": "Technology"
        }
        
        response = session.post(f"{BASE_URL}/api/complete-profile", json=profile_data)
        print(f"Create profile response: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Profile created successfully")
            result = response.json()
            print(f"Created profile: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Profile creation failed: {response.status_code} - {response.text}")
            return False
    
    # Step 4: Retrieve the profile (should work now)
    print("\n4. Retrieving profile for edit...")
    response = session.get(f"{BASE_URL}/api/complete-profile")
    print(f"Get profile response: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Failed to retrieve profile: {response.status_code} - {response.text}")
        return False
    
    current_profile = response.json()
    print("✅ Profile retrieved successfully")
    print(f"Current profile: {json.dumps(current_profile, indent=2)}")
    
    # Step 5: Update the profile using PUT
    print("\n5. Testing profile update (PUT)...")
    
    if 'profile' in current_profile:
        updated_profile = current_profile['profile'].copy()
        # Make some changes
        updated_profile['name'] = "Test User UPDATED"
        updated_profile['city'] = "Chennai"
        updated_profile['year_of_study'] = "4th Year"
        updated_profile['gpa_percentage'] = 9.0
        
        response = session.put(f"{BASE_URL}/api/complete-profile", json=updated_profile)
        print(f"Update profile response: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Profile updated successfully")
            result = response.json()
            print(f"Updated profile: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Profile update failed: {response.status_code} - {response.text}")
            return False
    
    # Step 6: Verify the update
    print("\n6. Verifying the update...")
    response = session.get(f"{BASE_URL}/api/complete-profile")
    
    if response.status_code == 200:
        final_profile = response.json()
        if final_profile['profile']['name'] == "Test User UPDATED":
            print("✅ Profile update verified successfully")
        else:
            print("❌ Profile update not reflected")
            return False
    else:
        print(f"❌ Failed to verify update: {response.status_code}")
        return False
    
    print("\n🎉 All tests passed! Edit profile functionality is working.")
    return True

if __name__ == "__main__":
    success = test_edit_profile_workflow()
    if not success:
        print("\n💥 Some tests failed!")
        exit(1)