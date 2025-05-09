import requests
import json
import time

def test_ollama_debug():
    """Debug Ollama API integration."""
    print("=== Ollama API Debug Test ===")
    
    # 1. Check if Ollama is running
    try:
        print("\nChecking if Ollama is running...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama is running!")
            models = response.json().get("models", [])
            if models:
                print(f"Available models: {', '.join([m.get('name', 'unknown') for m in models])}")
            else:
                print("No models found in the response.")
        else:
            print(f"✗ Ollama returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"✗ Error connecting to Ollama: {str(e)}")
        return
    
    # 2. Test a simple non-streaming request
    try:
        print("\nTesting non-streaming request...")
        payload = {
            "model": "tinyllama",
            "prompt": "What are common garden pests?",
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
        
        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            print("✓ Request successful!")
            
            # Try to parse the response
            try:
                result = response.json()
                print("\nResponse parsed successfully as JSON")
                
                if "response" in result:
                    print(f"Response content: {result['response'][:100]}...")
                else:
                    print(f"Response keys: {', '.join(result.keys())}")
                    print(f"Full response: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"✗ Error parsing response as JSON: {str(e)}")
                print(f"Raw response text: {response.text[:200]}...")
                
                # Check if it's a streaming response despite stream=False
                if '\n' in response.text:
                    print("\nDetected multiple lines in response, might be a streaming response")
                    lines = response.text.strip().split('\n')
                    print(f"Number of lines: {len(lines)}")
                    
                    for i, line in enumerate(lines[:3]):
                        print(f"\nLine {i+1}:")
                        try:
                            line_json = json.loads(line)
                            print(f"Parsed JSON: {json.dumps(line_json, indent=2)[:100]}...")
                        except json.JSONDecodeError:
                            print(f"Raw text: {line[:100]}...")
        else:
            print(f"✗ Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error making request: {str(e)}")
    
    # 3. Test a streaming request
    try:
        print("\nTesting streaming request...")
        payload = {
            "model": "tinyllama",
            "prompt": "List three common garden pests",
            "stream": True
        }
        
        response = requests.post("http://localhost:11434/api/generate", json=payload, stream=True, timeout=30)
        
        if response.status_code == 200:
            print("✓ Streaming request initiated successfully!")
            print("First few chunks of the response:")
            
            # Read the first few chunks
            chunk_count = 0
            for chunk in response.iter_lines():
                if chunk:
                    chunk_count += 1
                    print(f"\nChunk {chunk_count}:")
                    try:
                        chunk_json = json.loads(chunk)
                        if "response" in chunk_json:
                            print(f"Response text: {chunk_json['response']}")
                        else:
                            print(f"Chunk keys: {', '.join(chunk_json.keys())}")
                    except json.JSONDecodeError:
                        print(f"Raw chunk: {chunk.decode('utf-8')[:100]}")
                
                # Only show first 5 chunks
                if chunk_count >= 5:
                    print("\n... (more chunks available) ...")
                    break
            
            print(f"\nReceived {chunk_count} chunks in total")
        else:
            print(f"✗ Streaming request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error with streaming request: {str(e)}")
    
    print("\n=== Debug test completed ===")

if __name__ == "__main__":
    test_ollama_debug()
