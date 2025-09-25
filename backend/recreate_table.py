#!/usr/bin/env python3
"""
Simple script to recreate the complete_profiles table with new schema
"""

from app import create_app, db
from app.models import CompleteProfile
import sys

def recreate_complete_profiles_table():
    """Drop and recreate the complete_profiles table"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Dropping complete_profiles table if it exists...")
            # Drop the table if it exists
            CompleteProfile.__table__.drop(db.engine, checkfirst=True)
            
            print("Creating complete_profiles table with new schema...")
            # Create the table with new schema
            CompleteProfile.__table__.create(db.engine, checkfirst=True)
            
            print("Table recreated successfully!")
            return True
            
        except Exception as e:
            print(f"Error recreating table: {e}")
            return False

if __name__ == "__main__":
    print("Recreating complete_profiles table...")
    success = recreate_complete_profiles_table()
    if success:
        print("Table recreation completed successfully!")
    else:
        print("Table recreation failed!")
        sys.exit(1)