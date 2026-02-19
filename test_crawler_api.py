#!/usr/bin/env python3
"""
Test script for the Punjabi Crawler Flask API
"""

import requests
import json


def test_detect_punjabi():
    """Test the Punjabi detection endpoint."""
    url = "http://localhost:5000/api/detect-punjabi"
    test_cases = [
        "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਪੰਜਾਬੀ ਸੀਖਣ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰ ਰਹੀ ਹਾਂ।",
        "This is an English sentence.",
        "Punjabi news website",
        "ਪੰਜਾਬੀ ਗੀਤ ਸੁਣੋ",
        "Hello, how are you?"
    ]
    
    print("Testing Punjabi Detection API:")
    print("-" * 30)
    
    for text in test_cases:
        payload = {"text": text}
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            print(f"Text: '{text[:30]}...' -> Is Punjabi: {result['is_punjabi']}")
        except Exception as e:
            print(f"Error testing '{text[:20]}...': {e}")


def test_hello_api():
    """Test the hello endpoint."""
    url = "http://localhost:5000/api/hello"
    
    print("\nTesting Hello API:")
    print("-" * 20)
    
    try:
        response = requests.get(url)
        result = response.json()
        print(f"Response: {result['message']}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing Punjabi Crawler API")
    print("=" * 40)
    
    # Note: These tests will only work if the Flask app is running
    # Run 'python run.py' in another terminal to start the server first
    test_hello_api()
    test_detect_punjabi()
    
    print("\nNote: To run these tests properly, please start the Flask server first:")
    print("1. Run: python run.py")
    print("2. Then execute this test script")