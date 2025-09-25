"""
Add vision_vector_data and vision_processed_at columns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

app = create_app()

def add_vision_columns():
    """Add vision_vector_data and vision_processed_at columns"""
    
    with app.app_context():
        try:
            # SQL to add new columns
            alter_statements = [
                "ALTER TABLE users ADD COLUMN vision_vector_data TEXT NULL",
                "ALTER TABLE users ADD COLUMN vision_processed_at DATETIME NULL"
            ]
            
            print("Adding vision processing columns...")
            
            for statement in alter_statements:
                try:
                    with db.engine.connect() as connection:
                        connection.execute(db.text(statement))
                        connection.commit()
                    print(f"✓ Executed: {statement}")
                except Exception as e:
                    if "already exists" in str(e).lower() or "duplicate column name" in str(e).lower():
                        print(f"⚠ Column already exists, skipping: {statement}")
                    else:
                        print(f"✗ Error executing {statement}: {e}")
                        return False
            
            print("✓ Successfully added vision processing columns!")
            return True
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            return False

if __name__ == "__main__":
    add_vision_columns()