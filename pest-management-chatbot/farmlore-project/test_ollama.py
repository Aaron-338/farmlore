import requests
import sys
import json

print("Testing Ollama API from web container...")

# Test Tags API
try:
    print("Testing tags API...")
    r = requests.get('http://ollama:11434/api/tags', timeout=10)
    print(f'Status code: {r.status_code}')
    print(f'Response: {r.text[:100]}')
except Exception as e:
    print(f'Error: {e}')

# Test Generate API
try:
    print("\nTesting generate API...")
    payload = {
        "model": "tinyllama",
        "prompt": "Hello, how are you?"
    }
    r = requests.post('http://ollama:11434/api/generate', 
                      json=payload, 
                      timeout=30)
    print(f'Status code: {r.status_code}')
    print(f'Response: {r.text[:100]}')
except Exception as e:
    print(f'Error: {e}')