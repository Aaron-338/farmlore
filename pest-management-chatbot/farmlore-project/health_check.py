#!/usr/bin/env python
"""
Health check script for Docker containers.
This script checks the health of various services and exits with 0 if they are healthy,
or 1 if they are unhealthy.
"""

import sys
import os
import json
import argparse
import requests
from urllib.parse import urlparse

def check_web_service(url):
    """Check if the web service is running."""
    try:
        response = requests.get(url, headers={'Host': 'localhost'}, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Error checking web service: {str(e)}")
        return False

def check_ollama_service(url):
    """Check if the Ollama service is running."""
    try:
        # Just check if the tags endpoint responds, regardless of content
        response = requests.get(f"{url}/api/tags", timeout=5)
        if response.status_code == 200:
            # Verify there's at least one model
            data = response.json()
            if "models" in data and len(data["models"]) > 0:
                return True
            print("No models found in Ollama response")
            return False
        print(f"Non-200 status code from Ollama: {response.status_code}")
        return False
    except Exception as e:
        print(f"Error checking Ollama service: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Health check script')
    parser.add_argument('--service', choices=['web', 'ollama'], required=True,
                        help='Service to check')
    args = parser.parse_args()

    if args.service == 'web':
        url = "http://0.0.0.0:8000"
        if check_web_service(url):
            print("Web service is healthy")
            sys.exit(0)
        else:
            print("Web service is unhealthy")
            sys.exit(1)
    elif args.service == 'ollama':
        url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        if check_ollama_service(url):
            print("Ollama service is healthy")
            sys.exit(0)
        else:
            print("Ollama service is unhealthy")
            # Even if Ollama isn't ready, we don't want to restart the container
            # as it may be initializing models
            sys.exit(0)

if __name__ == "__main__":
    main() 