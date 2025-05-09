import requests
import json
import time

def test_end_to_end():
    """Test the end-to-end functionality of the chatbot with TinyLlama integration."""
    base_url = "http://localhost:8000/api/chat/"
    
    # Test conversation flow
    conversation = [
        "What pests affect tomatoes?",
        "Tell me more about aphids",
        "How can I control them?",
        "What's the procedure?",
        "Are there any biological controls?",
        "My cucumber plants have webbing on them",
        "What should I do?"
    ]
    
    for message in conversation:
        print(f"\n=== Sending: '{message}' ===")
        
        response = requests.post(
            base_url,
            json={
                "messages": [{"role": "user", "content": message}]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: '{data['message']['content']}'")
            print(f"Confidence: {data['metadata']['confidence']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        # Add a small delay between requests
        time.sleep(1)

if __name__ == "__main__":
    test_end_to_end()
