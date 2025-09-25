#!/usr/bin/env python3

from app.models import User, db
from app import create_app

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Found {len(users)} users:")
    
    for user in users:
        print(f"User ID: {user.user_id}")
        print(f"Name: {user.name}")
        print(f"Vision processed: {user.vision_processed_at}")
        print(f"Vision data: {'Yes' if user.vision_extracted_data else 'No'}")
        print(f"Vector data: {'Yes' if user.vision_vector_data else 'No'}")
        print("---")