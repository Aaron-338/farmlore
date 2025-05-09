"""
Management command to check and troubleshoot Ollama connectivity.

This command tests connectivity to various possible Ollama endpoints and
helps diagnose network issues between the web container and Ollama.
"""

import requests
import time
import socket
import json
from django.core.management.base import BaseCommand
from api.inference_engine.ollama_handler import OllamaHandler

class Command(BaseCommand):
    help = 'Check connectivity to Ollama service and troubleshoot issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix connectivity issues',
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=10,
            help='Connection timeout in seconds',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Ollama connectivity check...'))
        
        timeout = options['timeout']
        fix_mode = options['fix']
        
        # Possible Ollama endpoints to check
        endpoints = [
            'http://ollama:11434',
            'http://localhost:11434',
            'http://host.docker.internal:11434',
            'http://172.17.0.1:11434',  # Common Docker bridge network
        ]
        
        # Track successful endpoints
        successful_endpoints = []
        
        # Test each endpoint
        for endpoint in endpoints:
            self.stdout.write(f"Testing endpoint: {endpoint}")
            
            # Basic DNS resolution check
            hostname = endpoint.split('://')[1].split(':')[0]
            try:
                ip_address = socket.gethostbyname(hostname)
                self.stdout.write(self.style.SUCCESS(f"  DNS resolution successful: {hostname} -> {ip_address}"))
            except socket.gaierror:
                self.stdout.write(self.style.ERROR(f"  DNS resolution failed for {hostname}"))
                continue
            
            # API connectivity check
            try:
                response = requests.get(f"{endpoint}/api/tags", timeout=timeout)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"  Connection successful! Status code: {response.status_code}"))
                    models = response.json().get('models', [])
                    if models:
                        model_names = [model.get('model', 'unknown') for model in models]
                        self.stdout.write(self.style.SUCCESS(f"  Available models: {', '.join(model_names)}"))
                    else:
                        self.stdout.write(self.style.WARNING("  No models found"))
                    
                    successful_endpoints.append(endpoint)
                else:
                    self.stdout.write(self.style.ERROR(f"  Connection failed with status code: {response.status_code}"))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Connection error: {str(e)}"))
        
        # Summary
        if successful_endpoints:
            self.stdout.write(self.style.SUCCESS("\nConnectivity check complete. Successfully connected to:"))
            for endpoint in successful_endpoints:
                self.stdout.write(self.style.SUCCESS(f"  - {endpoint}"))
                
            # Test OllamaHandler with first successful endpoint
            self.stdout.write("\nTesting OllamaHandler with first successful endpoint...")
            handler = OllamaHandler(base_url=successful_endpoints[0])
            if handler.is_available:
                self.stdout.write(self.style.SUCCESS("OllamaHandler successfully connected!"))
                # Try a simple generation
                try:
                    response = handler.generate_response("Test", model="tinyllama")
                    self.stdout.write(self.style.SUCCESS(f"Test generation successful: {response[:50]}..."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Test generation failed: {str(e)}"))
            else:
                self.stdout.write(self.style.ERROR("OllamaHandler could not connect to Ollama"))
            
            # Apply fix if requested
            if fix_mode:
                self.fix_connectivity(successful_endpoints[0])
        else:
            self.stdout.write(self.style.ERROR("\nNo successful connections to any Ollama endpoint."))
            self.stdout.write(self.style.WARNING("Possible issues:"))
            self.stdout.write("  1. Ollama container is not running")
            self.stdout.write("  2. Network configuration issue between containers")
            self.stdout.write("  3. Firewall blocking the connection")
            self.stdout.write("  4. Ollama service is not ready yet")
            
            if fix_mode:
                self.stdout.write(self.style.WARNING("\nAttempting to fix connectivity issues..."))
                self.stdout.write("  Waiting for Ollama service to be available...")
                
                # Wait for Ollama to become available
                for _ in range(3):
                    time.sleep(30)  # Wait 30 seconds
                    self.stdout.write("  Retrying connectivity check...")
                    
                    for endpoint in endpoints:
                        try:
                            response = requests.get(f"{endpoint}/api/tags", timeout=timeout)
                            if response.status_code == 200:
                                self.stdout.write(self.style.SUCCESS(f"  Connected to {endpoint}!"))
                                self.fix_connectivity(endpoint)
                                return
                        except:
                            pass
                
                self.stdout.write(self.style.ERROR("  Could not establish connection after retries"))
    
    def fix_connectivity(self, working_endpoint):
        """Apply fixes for connectivity issues."""
        self.stdout.write(self.style.SUCCESS("\nApplying connectivity fixes..."))
        
        # Update .env file with working endpoint
        try:
            with open('.env', 'r') as f:
                env_content = f.read()
            
            if 'OLLAMA_BASE_URL=' in env_content:
                env_content = '\n'.join([
                    line if not line.startswith('OLLAMA_BASE_URL=') else f'OLLAMA_BASE_URL={working_endpoint}'
                    for line in env_content.split('\n')
                ])
            else:
                env_content += f'\nOLLAMA_BASE_URL={working_endpoint}\n'
            
            with open('.env', 'w') as f:
                f.write(env_content)
                
            self.stdout.write(self.style.SUCCESS("Updated .env file with working Ollama endpoint"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to update .env file: {str(e)}"))
        
        # Create a helper script for manual testing
        try:
            script_content = f"""#!/bin/bash
# Helper script to test Ollama connectivity

echo "Testing Ollama connectivity to {working_endpoint}..."
curl -s {working_endpoint}/api/tags
echo ""

echo "Testing basic generation with tinyllama model..."
curl -s {working_endpoint}/api/generate -d '{{"model": "tinyllama", "prompt": "Hello, world!", "stream": false}}'
echo ""

echo "Test complete!"
"""
            with open('test_ollama.sh', 'w') as f:
                f.write(script_content)
            
            import os
            os.chmod('test_ollama.sh', 0o755)
            self.stdout.write(self.style.SUCCESS("Created test_ollama.sh script for manual testing"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create helper script: {str(e)}"))
            
        self.stdout.write(self.style.SUCCESS("\nConnectivity fixes applied. Please restart the service to apply changes.")) 