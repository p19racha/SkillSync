#!/usr/bin/env python3
"""
Create a test user with a complete profile for edit testing
"""
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, '/Users/sathwikanumandla/Dev/ai-engine/backend')

from app import create_app, db
from app.models import User, CompleteProfile

def create_test_user_with_profile():
    """Create a test user with a complete profile for edit testing"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        username = "test_user_edit"
        
        # Get the existing user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ Test user '{username}' does not exist. Run create_test_user.py first.")
            return
        
        # Check if profile already exists by aadhar_id or user_id
        existing_profile = CompleteProfile.query.filter_by(user_id=user.id).first()
        
        if existing_profile:
            print(f"✅ Test user '{username}' already has a complete profile")
            print(f"   Profile details: {existing_profile.name}, {existing_profile.aadhar_id}")
            return
        
        # Create a complete profile
        profile = CompleteProfile(
            user_id=user.id,
            aadhar_id="555666777888",
            name="Test User Edit",
            dob=datetime.strptime("1995-05-15", "%Y-%m-%d").date(),
            age=28,  # calculated from DOB
            state="Karnataka",
            city="Bangalore", 
            pincode="560001",
            education_level="Undergraduate",
            degree="Computer Science",
            year_of_study="3rd Year",
            gpa_percentage=8.5,
            technical_skills="Python, JavaScript, React",
            internship_type_preference="Remote",
            duration_preference="3-6 months"
        )
        
        try:
            db.session.add(profile)
            db.session.commit()
            print(f"✅ Complete profile created for test user '{username}'")
            print(f"   Profile details: {profile.name}, {profile.aadhar_id}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Failed to create complete profile: {e}")

if __name__ == "__main__":
    create_test_user_with_profile()