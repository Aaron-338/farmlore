#!/usr/bin/env python
import docker

# Connect to Docker
client = docker.from_env()

# Define the test query
test_query = "How do I control aphids on my tomato plants?"

# Execute Python code in the container to check RAG matching
container = client.containers.get('farmlore-rag_connector-1')
result = container.exec_run(
    cmd=[
        "python", "-c",
        """
from standalone_rag import *
print('=== TESTING RAG MATCHING ===')
print(f'Query: {0}\\n')
print('=== PEST DATA TITLES ===')
for i, item in enumerate(PEST_DATA):
    print(f'{i+1}. {item["title"]}')
print('\\n=== TOP MATCHING RESULTS ===')
results = search_pest_data({0}, top_n=3)
for i, r in enumerate(results):
    print(f'MATCH {i+1}: {r["title"]} (Score: {r["score"]:.2f})')
print('\\n=== FIRST RESULT CONTENT ===')
if results: print(results[0]['content'][:300] + '...')
print('\\n=== APHID CONTROL ON TOMATOES ENTRY ===')
# Find and print the entry specifically about aphids on tomato plants
for item in PEST_DATA:
    if 'Aphid Control on Tomatoes' in item['title']:
        print(f'Title: {item["title"]}')
        print(f'Content sample: {item["content"][:300]}...')
        break
""".format(repr(test_query))
    ]
)

# Print the result
print(result.output.decode('utf-8')) 