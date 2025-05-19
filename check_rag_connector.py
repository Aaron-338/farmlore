#!/usr/bin/env python
import docker

# Connect to Docker
client = docker.from_env()
container = client.containers.get('farmlore-rag_connector-1')

# Create a test script
test_script = """
import inspect
import sys

try:
    # Check what's imported in the rag_web_connector module
    print("=== RAG Web Connector Imports ===")
    import rag_web_connector
    
    # Check the enhance_response function
    print("\\n=== Checking enhance_response function ===")
    if hasattr(rag_web_connector, 'enhance_response'):
        enhance_func = rag_web_connector.enhance_response
        print(f"Function source: {inspect.getmodule(enhance_func).__name__}")
    else:
        print("enhance_response not found in rag_web_connector")
    
    # Try to import both modules to check
    print("\\n=== Available RAG Modules ===")
    try:
        import standalone_rag
        print("standalone_rag module is available")
    except ImportError:
        print("standalone_rag module is NOT available")
    
    try:
        import improved_standalone_rag
        print("improved_standalone_rag module is available")
    except ImportError:
        print("improved_standalone_rag module is NOT available")
    
    # Test a query with the enhance_response function
    print("\\n=== Testing enhance_response ===")
    query = "How do I control aphids on my tomato plants?"
    response = "You should use insecticides."
    
    enhanced = rag_web_connector.enhance_response(query, response)
    print(f"Enhanced response mentions tomatoes: {'tomato' in enhanced.lower()}")
    print(f"Enhanced response mentions cucumbers: {'cucumber' in enhanced.lower()}")
    
except Exception as e:
    print(f"Error: {str(e)}")
"""

# Execute the test script in the container
print("Checking RAG web connector configuration...")
result = container.exec_run(["python", "-c", test_script])
print(result.output.decode('utf-8')) 