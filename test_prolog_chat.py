"""
Test script for the Prolog queries through the chat API
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_prolog_via_chat():
    """Test Prolog queries through the chat API"""
    try:
        # Test chat endpoint
        chat_url = "http://localhost:8000/api/chat/"
        
        # Prepare a series of test queries
        test_queries = [
            "What are common pests that attack tomato plants?",
            "How can I control aphids organically?",
            "Tell me about soil requirements for tomatoes",
            "What's the best way to prevent blight on tomatoes?",
            "Are there any indigenous methods to control pests on maize?"
        ]
        
        headers = {"Content-Type": "application/json"}
        
        for query in test_queries:
            # Prepare the request payload
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }
            
            logging.info(f"Testing query: {query}")
            logging.info(f"Payload: {json.dumps(payload)}")
            
            # Send the request
            response = requests.post(chat_url, json=payload, headers=headers, timeout=60)
            
            logging.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Response: {json.dumps(result, indent=2)}")
                # Add a separator for better readability
                logging.info("-" * 80)
            else:
                logging.error(f"Error: {response.text}")
                
    except Exception as e:
        logging.error(f"Error testing chat API: {str(e)}")

if __name__ == "__main__":
    test_prolog_via_chat() 