#!/usr/bin/env python3
"""
Test Ollama API call to debug the 500 error
"""

import requests
import json

def test_ollama_api():
    """Test basic Ollama API functionality"""
    
    api_endpoint = "http://localhost:11434/api/generate"
    
    # Simple text test first
    payload = {
        "model": "llama3.2-vision:latest",
        "prompt": "Hello, respond with just 'Working' if you can see this message.",
        "stream": False
    }
    
    try:
        print("🔄 Testing basic Ollama API...")
        response = requests.post(api_endpoint, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Response: {result.get('response', 'No response field')}")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

    # Test with format: json
    payload_json = {
        "model": "llama3.2-vision:latest", 
        "prompt": "Respond with a simple JSON object: {\"status\": \"working\"}",
        "stream": False,
        "format": "json"
    }
    
    try:
        print("\n🔄 Testing JSON format...")
        response = requests.post(api_endpoint, json=payload_json, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ JSON Response: {result.get('response', 'No response field')}")
        else:
            print(f"❌ JSON API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ JSON Request failed: {e}")

if __name__ == "__main__":
    test_ollama_api()