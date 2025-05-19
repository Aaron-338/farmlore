#!/usr/bin/env python
"""
RAG Chatbot

A simple chatbot CLI that demonstrates the RAG-enhanced API for agricultural queries.
"""
import os
import sys
import json
import time
import requests
from urllib.parse import urljoin

# Import the RAG components
from direct_api_rag_test import enhance_response

def call_api(query, timeout=60):
    """Call the API directly and return the response"""
    try:
        # Get base URL from environment or use default
        base_url = os.environ.get('API_URL', 'http://localhost:80')
        endpoint = '/api/chat/'
        
        # Build full URL
        url = urljoin(base_url, endpoint)
        
        # Prepare the request payload
        payload = {
            "message": query
        }
        
        # Send the request
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        
        # Check response status
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error calling API: {str(e)}")
        return None

def chat():
    """Run the chatbot with RAG enhancement"""
    print("=" * 60)
    print("🌱 FarmLore RAG-Enhanced Chatbot 🌱")
    print("=" * 60)
    print("Ask questions about agricultural pests and get RAG-enhanced responses.")
    print("Type 'exit', 'quit', or 'q' to end the conversation.")
    print("=" * 60)

    while True:
        # Get user input
        try:
            query = input("\n🧑‍🌾 You: ").strip()
        except EOFError:
            break
            
        # Check for exit commands
        if query.lower() in ['exit', 'quit', 'q', 'bye']:
            print("\nGoodbye! 👋")
            break
            
        if not query:
            continue
            
        # Process the query with the API
        print("\n🤖 Bot: Thinking...")
        api_response = call_api(query)
        
        if not api_response:
            print("I'm sorry, I couldn't process your request. Please try again.")
            continue
            
        # Extract the original response
        if 'response' in api_response:
            original_text = api_response['response']
        else:
            print("I received an unexpected response format. Please try again.")
            continue
        
        # Enhance with RAG
        enhanced_text = enhance_response(query, original_text)
        
        # Display the response
        print(f"\n🤖 Bot: {enhanced_text}")
        
        # Show enhancement info
        if enhanced_text != original_text:
            print("\n(Response was enhanced with RAG information)")

if __name__ == "__main__":
    chat() 