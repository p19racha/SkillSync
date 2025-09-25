#!/usr/bin/env python3
"""
Test automatic document processing for existing users
"""

from app.models import User, db
from app import create_app
import sys
import os

# Add Engine path for imports
engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Engine')
sys.path.append(engine_path)

from main import RecommendationOrchestrator

app = create_app()

def test_automatic_processing():
    """Test the automatic document processing workflow"""
    
    with app.app_context():
        # Get user AUiT01 who has uploaded documents
        user = User.query.filter_by(user_id='AUiT01').first()
        
        if not user:
            print("❌ User AUiT01 not found")
            return
        
        print(f"🔄 Processing documents for user: {user.user_id} ({user.name})")
        
        # Initialize the orchestrator
        try:
            orchestrator = RecommendationOrchestrator()
            print("✅ RecommendationOrchestrator initialized")
            
            # Get uploaded files for this user
            upload_path = os.path.join('uploads', 'certifications', user.user_id)
            file_paths = []
            
            if os.path.exists(upload_path):
                for filename in os.listdir(upload_path):
                    if filename.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                        file_paths.append(os.path.join(upload_path, filename))
            
            print(f"📁 Found {len(file_paths)} files to process: {file_paths}")
            
            if not file_paths:
                print("⚠️ No files found to process")
                return
                
            # Process documents using the backend function (which saves to database)
            from app.routes import process_user_documents_automatically
            result = process_user_documents_automatically(user.user_id)
            print(f"📊 Processing result: {result}")
            
            # Check if data was updated
            db.session.refresh(user)
            print(f"Vision processed at: {user.vision_processed_at}")
            print(f"Vision data available: {'Yes' if user.vision_extracted_data else 'No'}")
            print(f"Vector data available: {'Yes' if user.vision_vector_data else 'No'}")
            
            if user.vision_extracted_data:
                print("✅ Automatic processing successful!")
            else:
                print("⚠️ Processing completed but no data extracted")
                
        except Exception as e:
            print(f"❌ Error during processing: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_automatic_processing()