#!/usr/bin/env python3
"""
Test VisionProcessor with actual files to debug the issue
"""

import sys
import os
import base64

# Add Engine path
engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Engine')
sys.path.append(engine_path)

from ai_processing.vision_processor import VisionProcessor

def test_vision_processor():
    """Test VisionProcessor with actual uploaded files"""
    
    # Initialize processor
    processor = VisionProcessor()
    print("✅ VisionProcessor initialized")
    
    # Test file paths
    test_files = [
        'uploads/certifications/AUiT01/ICICI_FY24-25__Dayakar_20250924_121303.pdf',
        'uploads/certifications/AUiT01/sudo-code_20250924_111433.pdf'
    ]
    
    for file_path in test_files:
        print(f"\n🔄 Testing file: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"✅ File exists, size: {os.path.getsize(file_path)} bytes")
        
        # Try to encode the file
        try:
            if file_path.lower().endswith('.pdf'):
                print("📄 PDF file detected")
                # For PDFs, we might need to convert to image first
                # For now, let's see what happens
            
            with open(file_path, 'rb') as f:
                file_content = f.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                print(f"✅ File encoded successfully, encoded size: {len(encoded_content)}")
                
                # Check if encoded content is too large for API
                if len(encoded_content) > 1000000:  # 1MB limit roughly
                    print("⚠️ Encoded file might be too large for API")
                
        except Exception as e:
            print(f"❌ File encoding failed: {e}")
            continue
        
        # Test extraction
        try:
            print("🔄 Testing document extraction...")
            result = processor.extract_from_document(file_path, "certificate")
            
            if result.get('success'):
                print(f"✅ Extraction successful!")
                print(f"📊 Extracted data keys: {list(result.get('extracted_data', {}).keys())}")
            else:
                print(f"❌ Extraction failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Extraction exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_vision_processor()