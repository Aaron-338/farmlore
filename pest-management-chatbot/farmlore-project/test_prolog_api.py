"""
Test script for the Prolog query API
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_prolog_query():
    """Test the Prolog query API"""
    try:
        # Test Prolog endpoint
        prolog_url = "http://localhost:8000/chatbot/prolog_query_api"
        
        # Test different query types
        query_types = [
            {
                "query_type": "pest_solutions",
                "pest": "aphids",
                "region": "global"
            },
            {
                "query_type": "recommend",
                "pest": "aphids"
            },
            {
                "query_type": "pest_info",
                "pest": "aphids"
            }
        ]
        
        headers = {"Content-Type": "application/json"}
        
        for query in query_types:
            logging.info(f"Testing query type: {query['query_type']}")
            logging.info(f"Payload: {json.dumps(query)}")
            
            # Send the request
            response = requests.post(prolog_url, json=query, headers=headers, timeout=60)
            
            logging.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Response: {json.dumps(result, indent=2)}")
            else:
                logging.error(f"Error: {response.text}")
                
    except Exception as e:
        logging.error(f"Error testing Prolog API: {str(e)}")

if __name__ == "__main__":
    test_prolog_query() 