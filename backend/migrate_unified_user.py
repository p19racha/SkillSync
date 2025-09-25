#!/usr/bin/env python3
"""
Migration script to merge users and complete_profiles tables into a unified users table.
This script handles the database schema migration safely.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from datetime import datetime
import string
import random
from sqlalchemy import text

def generate_user_id():
    """Generate a random 6-character alphanumeric user ID"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def backup_tables():
    """Create backup of existing tables"""
    print("Creating backup of existing tables...")
    
    try:
        # Backup users table
        db.session.execute(text("CREATE TABLE users_backup AS SELECT * FROM users"))
        print("✓ users table backed up to users_backup")
        
        # Backup complete_profiles table if it exists
        result = db.session.execute(text("SHOW TABLES LIKE 'complete_profiles'"))
        if result.fetchone():
            db.session.execute(text("CREATE TABLE complete_profiles_backup AS SELECT * FROM complete_profiles"))
            print("✓ complete_profiles table backed up to complete_profiles_backup")
        
        db.session.commit()
        return True
    except Exception as e:
        print(f"❌ Error creating backups: {e}")
        db.session.rollback()
        return False

def get_existing_data():
    """Get existing data from both tables"""
    print("Retrieving existing data...")
    
    try:
        # Get users data
        users_result = db.session.execute(text("SELECT * FROM users"))
        users_data = [dict(row._mapping) for row in users_result]
        print(f"✓ Found {len(users_data)} users")
        
        # Get complete_profiles data if table exists
        profiles_data = []
        result = db.session.execute(text("SHOW TABLES LIKE 'complete_profiles'"))
        if result.fetchone():
            profiles_result = db.session.execute(text("SELECT * FROM complete_profiles"))
            profiles_data = [dict(row._mapping) for row in profiles_result]
            print(f"✓ Found {len(profiles_data)} complete profiles")
        
        return users_data, profiles_data
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")
        return [], []

def drop_old_tables():
    """Drop the old table structure"""
    print("Dropping old table structure...")
    
    try:
        # Drop foreign key constraints first
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Drop complete_profiles table if it exists
        result = db.session.execute(text("SHOW TABLES LIKE 'complete_profiles'"))
        if result.fetchone():
            db.session.execute(text("DROP TABLE complete_profiles"))
            print("✓ complete_profiles table dropped")
        
        # Drop old users table
        db.session.execute(text("DROP TABLE users"))
        print("✓ users table dropped")
        
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()
        return True
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        db.session.rollback()
        return False

def create_new_table():
    """Create the new unified users table"""
    print("Creating new unified users table...")
    
    try:
        db.create_all()
        print("✓ New users table created with unified schema")
        return True
    except Exception as e:
        print(f"❌ Error creating new table: {e}")
        return False

def migrate_data(users_data, profiles_data):
    """Migrate data to the new unified table"""
    print("Migrating data to unified table...")
    
    # Create lookup for profiles by user_id
    profiles_by_user_id = {profile['user_id']: profile for profile in profiles_data}
    
    migrated_count = 0
    
    try:
        for user_data in users_data:
            # Generate new user_id
            user_id = generate_user_id()
            
            # Ensure unique user_id
            while db.session.execute(text("SELECT user_id FROM users WHERE user_id = :user_id"), {'user_id': user_id}).fetchone():
                user_id = generate_user_id()
            
            # Get profile data if it exists
            old_user_id = user_data['id']
            profile_data = profiles_by_user_id.get(old_user_id, {})
            
            # Create new user with merged data
            new_user = User(
                username=user_data['username'],
                password='dummy'  # Will be replaced with actual hash
            )
            new_user.user_id = user_id
            new_user.password = user_data['password']  # Keep original hash
            new_user.created_at = user_data['created_at']
            new_user.is_active = user_data.get('is_active', True)
            
            # Add profile data if available
            if profile_data:
                new_user.aadhar_id = profile_data.get('aadhar_id')
                new_user.name = profile_data.get('name')
                new_user.dob = profile_data.get('dob')
                new_user.age = profile_data.get('age')
                new_user.state = profile_data.get('state')
                new_user.city = profile_data.get('city')
                new_user.pincode = profile_data.get('pincode')
                new_user.education_level = profile_data.get('education_level')
                new_user.degree = profile_data.get('degree')
                new_user.year_of_study = profile_data.get('year_of_study')
                new_user.gpa_percentage = profile_data.get('gpa_percentage')
                new_user.relevant_courses = profile_data.get('relevant_courses')
                new_user.technical_skills = profile_data.get('technical_skills')
                new_user.soft_skills = profile_data.get('soft_skills')
                new_user.certifications = profile_data.get('certifications')
                new_user.previous_internships = profile_data.get('previous_internships')
                new_user.projects = profile_data.get('projects')
                new_user.hackathons_competitions = profile_data.get('hackathons_competitions')
                new_user.research_experience = profile_data.get('research_experience')
                new_user.internship_type_preference = profile_data.get('internship_type_preference')
                new_user.duration_preference = profile_data.get('duration_preference')
                new_user.stipend_expectation = profile_data.get('stipend_expectation')
                new_user.preferred_industry = profile_data.get('preferred_industry')
                new_user.profile_updated_at = profile_data.get('updated_at')
            
            db.session.add(new_user)
            migrated_count += 1
        
        db.session.commit()
        print(f"✓ Successfully migrated {migrated_count} users")
        return True
        
    except Exception as e:
        print(f"❌ Error migrating data: {e}")
        db.session.rollback()
        return False

def verify_migration():
    """Verify the migration was successful"""
    print("Verifying migration...")
    
    try:
        user_count = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar()
        print(f"✓ New users table contains {user_count} records")
        
        # Check a few sample records
        sample_users = db.session.execute(text("SELECT user_id, username FROM users LIMIT 5")).fetchall()
        print("Sample migrated users:")
        for user in sample_users:
            print(f"  - {user[1]} (ID: {user[0]})")
        
        return True
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

def main():
    """Main migration function"""
    print("=" * 50)
    print("UNIFIED USER TABLE MIGRATION")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        print("Starting migration process...")
        
        # Step 1: Backup existing tables
        if not backup_tables():
            print("❌ Migration failed at backup step")
            return False
        
        # Step 2: Get existing data
        users_data, profiles_data = get_existing_data()
        if not users_data:
            print("❌ No user data found to migrate")
            return False
        
        # Step 3: Drop old tables
        if not drop_old_tables():
            print("❌ Migration failed at table drop step")
            return False
        
        # Step 4: Create new table
        if not create_new_table():
            print("❌ Migration failed at table creation step")
            return False
        
        # Step 5: Migrate data
        if not migrate_data(users_data, profiles_data):
            print("❌ Migration failed at data migration step")
            return False
        
        # Step 6: Verify migration
        if not verify_migration():
            print("❌ Migration verification failed")
            return False
        
        print("\n" + "=" * 50)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nBackup tables created:")
        print("- users_backup (contains original users data)")
        print("- complete_profiles_backup (contains original profile data)")
        print("\nYou can drop these backup tables once you're confident the migration worked.")
        
        return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)