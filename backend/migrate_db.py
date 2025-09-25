#!/usr/bin/env python3
"""
Database migration script to update the complete_profiles table
with new schema (dob, age, state, city, pincode instead of age, location)
"""

import mysql.connector
from datetime import datetime, date
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_db_connection():
    """Get database connection using the same credentials as the app"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='myuser',
            password='mypassword',
            database='login_system'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def check_table_exists(cursor, table_name):
    """Check if a table exists"""
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.tables 
        WHERE table_schema = 'login_system' 
        AND table_name = '{table_name}'
    """)
    return cursor.fetchone()[0] > 0

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.columns 
        WHERE table_schema = 'login_system' 
        AND table_name = '{table_name}' 
        AND column_name = '{column_name}'
    """)
    return cursor.fetchone()[0] > 0

def migrate_complete_profiles_table():
    """Migrate the complete_profiles table to new schema"""
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Check if table exists
        if not check_table_exists(cursor, 'complete_profiles'):
            print("complete_profiles table doesn't exist yet - no migration needed")
            return True
        
        print("Starting migration of complete_profiles table...")
        
        # Check what columns exist
        age_exists = check_column_exists(cursor, 'complete_profiles', 'age')
        location_exists = check_column_exists(cursor, 'complete_profiles', 'location')
        dob_exists = check_column_exists(cursor, 'complete_profiles', 'dob')
        state_exists = check_column_exists(cursor, 'complete_profiles', 'state')
        city_exists = check_column_exists(cursor, 'complete_profiles', 'city')
        pincode_exists = check_column_exists(cursor, 'complete_profiles', 'pincode')
        
        print(f"Current schema - age: {age_exists}, location: {location_exists}")
        print(f"New schema - dob: {dob_exists}, state: {state_exists}, city: {city_exists}, pincode: {pincode_exists}")
        
        # If we have old schema and not new schema, migrate
        if age_exists and location_exists and not (dob_exists and state_exists):
            print("Migrating from old schema to new schema...")
            
            # First, get existing data
            cursor.execute("SELECT aadhar_id, age, location FROM complete_profiles")
            existing_data = cursor.fetchall()
            print(f"Found {len(existing_data)} existing profiles to migrate")
            
            # Add new columns
            if not dob_exists:
                print("Adding dob column...")
                cursor.execute("ALTER TABLE complete_profiles ADD COLUMN dob DATE")
            
            if not state_exists:
                print("Adding state column...")
                cursor.execute("ALTER TABLE complete_profiles ADD COLUMN state VARCHAR(50)")
            
            if not city_exists:
                print("Adding city column...")
                cursor.execute("ALTER TABLE complete_profiles ADD COLUMN city VARCHAR(50)")
            
            if not pincode_exists:
                print("Adding pincode column...")
                cursor.execute("ALTER TABLE complete_profiles ADD COLUMN pincode VARCHAR(6)")
            
            # Update existing records with estimated data
            for aadhar_id, age, location in existing_data:
                # Estimate date of birth from age
                current_year = datetime.now().year
                birth_year = current_year - age
                estimated_dob = date(birth_year, 1, 1)  # Estimate Jan 1st
                
                # Parse location (assume format like "City, State" or just "City")
                location_parts = location.split(',') if location else ['Unknown', 'Unknown']
                if len(location_parts) >= 2:
                    city = location_parts[0].strip()
                    state = location_parts[1].strip()
                else:
                    city = location_parts[0].strip() if location_parts else 'Unknown'
                    state = 'Unknown'
                
                # Update the record
                cursor.execute("""
                    UPDATE complete_profiles 
                    SET dob = %s, state = %s, city = %s, pincode = %s 
                    WHERE aadhar_id = %s
                """, (estimated_dob, state, city, '000000', aadhar_id))
                
                print(f"Migrated profile {aadhar_id}: age {age} -> dob {estimated_dob}, location '{location}' -> state '{state}', city '{city}'")
            
            # Make new columns NOT NULL after populating them
            print("Making new columns NOT NULL...")
            cursor.execute("ALTER TABLE complete_profiles MODIFY COLUMN dob DATE NOT NULL")
            cursor.execute("ALTER TABLE complete_profiles MODIFY COLUMN state VARCHAR(50) NOT NULL")
            cursor.execute("ALTER TABLE complete_profiles MODIFY COLUMN city VARCHAR(50) NOT NULL")
            cursor.execute("ALTER TABLE complete_profiles MODIFY COLUMN pincode VARCHAR(6) NOT NULL")
            
            # Drop old columns
            print("Dropping old columns...")
            cursor.execute("ALTER TABLE complete_profiles DROP COLUMN location")
            
            print("Migration completed successfully!")
            
        elif dob_exists and state_exists:
            print("Table already has new schema - no migration needed")
            
        else:
            print("Unknown schema state - manual intervention may be required")
        
        connection.commit()
        return True
        
    except mysql.connector.Error as e:
        print(f"Database error during migration: {e}")
        connection.rollback()
        return False
    except Exception as e:
        print(f"Unexpected error during migration: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Starting database migration...")
    success = migrate_complete_profiles_table()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        sys.exit(1)