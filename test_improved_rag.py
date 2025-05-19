#!/usr/bin/env python
import requests
import json

# Define the test queries
TEST_QUERIES = [
    {
        "name": "Aphids on Tomatoes",
        "query": "How do I control aphids on my tomato plants?",
        "response": "You should use insecticides."
    },
    {
        "name": "Pests on Tomatoes",
        "query": "What pests affect tomato plants?",
        "response": "Tomato plants can be affected by various pests."
    },
    {
        "name": "Aphids on Roses",
        "query": "How do I treat aphids on roses?",
        "response": "Aphids on roses can be treated with insecticides or natural predators."
    }
]

# Deploy the improved RAG module to the container
def deploy_improved_rag():
    print("Deploying improved RAG module...")
    
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get('farmlore-rag_connector-1')
        
        # Copy the improved RAG module to the container
        with open('patched_standalone_rag.py', 'r') as f:
            improved_rag_code = f.read()
            
        # Create a deployment script
        deploy_script = f"""
import os

# Write improved RAG module to a temporary file
with open('/app/improved_standalone_rag.py', 'w') as f:
    f.write({repr(improved_rag_code)})

# Test the improved RAG module
print("Testing improved RAG module...")
exec(open('/app/improved_standalone_rag.py').read())

# Modify rag_web_connector.py to use the improved RAG module
print("Updating web connector to use improved RAG...")
with open('/app/rag_web_connector.py', 'r') as f:
    content = f.read()

# Replace the import for standalone_rag with improved version
if 'from standalone_rag import' in content:
    content = content.replace(
        'from standalone_rag import enhance_response, search_pest_data', 
        'from improved_standalone_rag import enhance_response, search_pest_data_improved as search_pest_data'
    )
    content = content.replace(
        'from standalone_rag import enhance_response', 
        'from improved_standalone_rag import enhance_response'
    )

# Write the updated web connector
with open('/app/rag_web_connector.py', 'w') as f:
    f.write(content)

print("Deployment complete!")
print("Restarting Flask server...")
"""
        
        # Execute the deployment script
        container.exec_run(["python", "-c", deploy_script])
        
        # Restart the container to apply changes
        print("Restarting RAG connector container...")
        container.restart()
        
        print("Improved RAG module deployed successfully!")
        return True
        
    except Exception as e:
        print(f"Error deploying improved RAG module: {e}")
        return False

# Test the improved RAG module
def test_improved_rag():
    print("\nTesting improved RAG module...")
    
    for test in TEST_QUERIES:
        print(f"\n=== Testing: {test['name']} ===")
        print(f"Query: {test['query']}")
        print(f"Original response: {test['response']}")
        
        try:
            # Send request to RAG enhance endpoint
            response = requests.post(
                "http://localhost/rag-api/rag-enhance",
                json={"query": test['query'], "response": test['response']},
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Print enhancement status
                if data.get('was_enhanced', False):
                    # Extract just the enhancement
                    original = data.get('original', '')
                    enhanced = data.get('enhanced', '')
                    enhancement = enhanced.replace(original, "").strip()
                    
                    print("\nEnhancement successful!")
                    print(f"\nEnhancement title: {enhancement.split('\n')[0] if '\n' in enhancement else 'N/A'}")
                else:
                    print("\nNo enhancement was applied.")
            else:
                print(f"\nError: Received status code {response.status_code}")
                
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    # Deploy and test the improved RAG module
    if deploy_improved_rag():
        # Wait for the container to restart
        import time
        print("Waiting for container to restart...")
        time.sleep(5)
        
        # Test the improved RAG module
        test_improved_rag() 