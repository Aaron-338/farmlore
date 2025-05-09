"""
Test script for the chatbot interface
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_chat():
    """Test the chat interface"""
    try:
        # Test chat endpoint
        chat_url = "http://localhost:8000/api/chat/"
        
        # Prepare the request payload in the correct format
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": "How do I control aphids on tomato plants?"
                }
            ]
        }
        
        logging.info(f"Testing chat API at: {chat_url}")
        logging.info(f"Payload: {json.dumps(payload)}")
        
        # Send the request
        headers = {"Content-Type": "application/json"}
        response = requests.post(chat_url, json=payload, headers=headers, timeout=60)
        
        logging.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logging.info(f"Response: {json.dumps(result, indent=2)}")
        else:
            logging.error(f"Error: {response.text}")
            
    except Exception as e:
        logging.error(f"Error testing chat API: {str(e)}")

if __name__ == "__main__":
    test_chat() 