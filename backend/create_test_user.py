#!/usr/bin/env python3
"""
Create a test user for authentication testing
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/Users/sathwikanumandla/Dev/ai-engine/backend')

from app import create_app, db
from app.models import User

def create_test_user():
    """Create a test user for authentication testing"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        username = "test_user_edit"
        password = "test123"
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"✅ Test user '{username}' already exists")
            return
        
        # Create new user
        user = User(username=username, password=password)
        
        try:
            db.session.add(user)
            db.session.commit()
            print(f"✅ Test user '{username}' created successfully")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Failed to create test user: {e}")

if __name__ == "__main__":
    create_test_user()