#!/usr/bin/env python3
"""
Debug the profile-user relationship
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/Users/sathwikanumandla/Dev/ai-engine/backend')

from app import create_app, db
from app.models import User, CompleteProfile

def debug_profile_relationship():
    """Debug why the profile isn't being found"""
    app = create_app()
    
    with app.app_context():
        username = "test_user_edit"
        
        # Get the user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ User '{username}' not found")
            return
        
        print(f"✅ User found: {user.username} (ID: {user.id})")
        
        # Look for profiles by user_id
        profiles_by_user_id = CompleteProfile.query.filter_by(user_id=user.id).all()
        print(f"Profiles found by user_id {user.id}: {len(profiles_by_user_id)}")
        
        for profile in profiles_by_user_id:
            print(f"  - Profile: {profile.name}, Aadhar: {profile.aadhar_id}, User ID: {profile.user_id}")
        
        # Look for all profiles to see what exists
        all_profiles = CompleteProfile.query.all()
        print(f"\nAll profiles in database: {len(all_profiles)}")
        
        for profile in all_profiles:
            print(f"  - Profile: {profile.name}, Aadhar: {profile.aadhar_id}, User ID: {profile.user_id}")
            
        # Check the user's has_complete_profile property
        print(f"\nUser.has_complete_profile: {user.has_complete_profile}")

if __name__ == "__main__":
    debug_profile_relationship()