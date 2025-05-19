#!/usr/bin/env python
import docker

# Connect to Docker
client = docker.from_env()
container = client.containers.get('farmlore-rag_connector-1')

# Fix the import in rag_web_connector.py
print("Fixing imports in rag_web_connector.py...")
result = container.exec_run(
    cmd=[
        "python", "-c",
        """
import os

# Read the current connector file
with open('/app/rag_web_connector.py', 'r') as f:
    content = f.read()

# Replace the import statements
content = content.replace(
    'from standalone_rag import enhance_response, search_pest_data',
    'from improved_standalone_rag import enhance_response, search_pest_data_improved as search_pest_data'
)

# Write the updated file
with open('/app/rag_web_connector.py', 'w') as f:
    f.write(content)

print("Successfully updated rag_web_connector.py to use improved_standalone_rag")
"""
    ]
)

print(result.output.decode('utf-8'))

# Restart the container
print("Restarting the RAG connector container...")
container.restart()
print("Container restarted. The improved RAG system should now be active.") 