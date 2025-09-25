#!/usr/bin/env python3
"""
Test script for the enhanced complete profile functionality
"""

import requests
import json
from datetime import date

# Base URL
BASE_URL = "http://127.0.0.1:5001"

def test_profile_creation():
    """Test creating a profile with new schema"""
    
    # First register/login a test user
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123"
    }
    
    # Try to register (might fail if user exists)
    response = requests.post(f"{BASE_URL}/api/register", json=register_data)
    print(f"Register response: {response.status_code}")
    
    # Login
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/api/login", json=login_data)
    print(f"Login response: {response.status_code} - {response.json()}")
    
    if response.status_code != 200:
        print("Login failed!")
        return False
    
    # Test profile creation with new schema
    profile_data = {
        "aadhar_id": "123456789012",
        "name": "Test User",
        "dob": "1995-06-15",  # New: Date of birth instead of age
        "state": "Karnataka",  # New: State instead of location
        "city": "Bangalore",  # New: City
        "pincode": "560001",  # New: Pincode
        "education_level": "Undergraduate",
        "degree": "B.Tech Computer Science",
        "year_of_study": "3rd Year",
        "gpa_percentage": 8.5,
        "relevant_courses": "Data Structures, Algorithms, Web Development",
        "technical_skills": "Python, JavaScript, React",
        "soft_skills": "Communication, Leadership",
        "previous_internships": "Summer intern at Tech Corp",
        "projects": "E-commerce website, Chat application",
        "hackathons_competitions": "Won first prize in college hackathon",
        "research_experience": "AI research project",
        "internship_type_preference": "Hybrid",
        "duration_preference": "3-6 months",
        "stipend_expectation": "10k-25k",
        "preferred_industry": "Technology, Finance"
    }
    
    # Create profile
    response = session.post(f"{BASE_URL}/api/complete-profile", json=profile_data)
    print(f"Create profile response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Profile created: {data['success']}")
        if data['success']:
            print(f"Profile data: {json.dumps(data['profile'], indent=2)}")
    else:
        print(f"Error: {response.text}")
        return False
    
    # Test profile retrieval
    response = session.get(f"{BASE_URL}/api/complete-profile")
    print(f"Get profile response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Profile retrieved: {data['success']}")
        if data['success']:
            retrieved_profile = data['profile']
            print(f"Retrieved profile age: {retrieved_profile['age']} (calculated from DOB)")
            print(f"Retrieved profile location: {retrieved_profile['state']}, {retrieved_profile['city']}, {retrieved_profile['pincode']}")
    else:
        print(f"Error: {response.text}")
        return False
    
    # Test profile update (PUT)
    update_data = {
        "aadhar_id": "123456789012",
        "name": "Test User Updated",
        "dob": "1995-06-15",
        "state": "Tamil Nadu",  # Changed state
        "city": "Chennai",      # Changed city
        "pincode": "600001",    # Changed pincode
        "education_level": "Undergraduate",
        "degree": "B.Tech Computer Science",
        "year_of_study": "4th Year",  # Updated year
        "gpa_percentage": 9.0,        # Updated GPA
        "relevant_courses": "Data Structures, Algorithms, Web Development, Machine Learning",
        "technical_skills": "Python, JavaScript, React, Node.js",
        "soft_skills": "Communication, Leadership, Problem Solving",
        "previous_internships": "Summer intern at Tech Corp, Winter intern at Startup",
        "projects": "E-commerce website, Chat application, ML project",
        "hackathons_competitions": "Won first prize in college hackathon, Second place in national competition",
        "research_experience": "AI research project, Published paper",
        "internship_type_preference": "Remote",
        "duration_preference": "6+ months",
        "stipend_expectation": "25k+",
        "preferred_industry": "Technology, Finance, Healthcare"
    }
    
    response = session.put(f"{BASE_URL}/api/complete-profile", json=update_data)
    print(f"Update profile response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Profile updated: {data['success']}")
        if data['success']:
            print(f"Updated profile data: {json.dumps(data['profile'], indent=2)}")
    else:
        print(f"Error: {response.text}")
        return False
    
    print("All tests passed!")
    return True

if __name__ == "__main__":
    print("Testing enhanced complete profile functionality...")
    success = test_profile_creation()
    if success:
        print("✅ All tests passed successfully!")
    else:
        print("❌ Some tests failed!")