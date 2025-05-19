#!/usr/bin/env python
import docker

# Connect to Docker
client = docker.from_env()
container = client.containers.get('farmlore-rag_connector-1')

# Create a test script
test_script = """
try:
    from improved_standalone_rag import search_pest_data_improved
    
    # Test query
    query = "How do I control aphids on my tomato plants?"
    
    # Get results
    results = search_pest_data_improved(query)
    
    # Print top result
    print(f"Top result: {results[0]['title']} (Score: {results[0]['score']:.2f})")
    
    # Print all results
    print("\\nAll results:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['title']} (Score: {result['score']:.2f})")
        
except Exception as e:
    print(f"Error: {str(e)}")
"""

# Execute the test script in the container
print("Testing improved search function in the container...")
result = container.exec_run(["python", "-c", test_script])
print(result.output.decode('utf-8')) 