#!/usr/bin/env python
"""
RAG Web Connector

A Flask server that serves as a bridge between the web chat interface and our RAG enhancement.
"""
import os
import sys
import json
import logging
import requests
import time
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, Response, stream_with_context
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("rag_web_connector")

# Simple in-memory cache for API responses
response_cache = {}
CACHE_TTL = 3600  # Cache TTL in seconds (1 hour)

def get_cache_key(message):
    """Generate a cache key for a message"""
    return hashlib.md5(message.encode('utf-8')).hexdigest()

def get_cached_response(message):
    """Get a cached response if available and not expired"""
    cache_key = get_cache_key(message)
    if cache_key in response_cache:
        cached_item = response_cache[cache_key]
        if datetime.now() < cached_item['expires']:
            logger.info(f"Cache hit for message: {message[:30]}...")
            return cached_item['response']
    return None

def cache_response(message, response):
    """Cache a response with expiration time"""
    cache_key = get_cache_key(message)
    response_cache[cache_key] = {
        'response': response,
        'expires': datetime.now() + timedelta(seconds=CACHE_TTL)
    }
    logger.info(f"Cached response for message: {message[:30]}...")
    
    # Clean old cache entries
    clean_expired_cache()
    
def clean_expired_cache():
    """Remove expired entries from cache"""
    now = datetime.now()
    expired_keys = [key for key, item in response_cache.items() if now > item['expires']]
    for key in expired_keys:
        del response_cache[key]
    
    if expired_keys:
        logger.info(f"Removed {len(expired_keys)} expired cache entries")

# Import the RAG enhancement function from standalone_rag module
# TRY:
#     from improved_standalone_rag import enhance_response, search_pest_data_improved as search_pest_data
#     logger.info("Successfully imported standalone_rag module")
# EXCEPT ImportError:
#     # If it fails, define a basic implementation
#     logger.warning("Could not import standalone_rag module, using basic implementation")
#     def enhance_response(query, response):
#         logger.warning("Using placeholder enhance_response function")
#         return response
logger.info("Local RAG enhancement in rag_web_connector is now disabled. Web service is responsible for RAG.")

# Set up the Flask app
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy'}), 200

# Get API URL from environment or use default
API_URL = os.environ.get('API_URL', 'http://web:8000')
API_ENDPOINT = '/api/chat/'

@app.route('/rag-enhance', methods=['POST'])
def rag_enhance():
    """
    Endpoint to enhance responses with RAG
    
    Takes a user query and original response, returns the RAG-enhanced response
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        query = data.get('query')
        original_response = data.get('response')
        
        if not query or not original_response:
            return jsonify({
                'success': False,
                'error': 'Missing query or response'
            }), 400
            
        logger.info(f"Enhancing response for query: {query}")
        
        # Apply RAG enhancement
        # enhanced_response = enhance_response(query, original_response)
        
        # Determine if enhancement was applied
        # was_enhanced = enhanced_response != original_response
        
        return jsonify({
            'success': True,
            'original': original_response,
            'enhanced': original_response,
            'was_enhanced': False
        })
        
    except Exception as e:
        logger.error(f"Error enhancing response: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _try_direct_ollama_api(self, prompt, model="tinyllama"):
    """Try to call Ollama API directly with multiple fallback endpoints."""
    fallback_urls = [
        "http://ollama:11434",
        "http://localhost:11434",
        "http://host.docker.internal:11434",
        "http://172.17.0.1:11434"
    ]
    
    for base_url in fallback_urls:
        try:
            api_url = f"{base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            logger.info(f"Trying direct Ollama API call to {api_url}")
            response = requests.post(api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    logger.info(f"Direct API call successful to {base_url}")
                    return result["response"]
            
        except Exception as e:
            logger.warning(f"Direct API call to {base_url} failed: {str(e)}")
            continue
    
    return None

@app.route('/proxy-api', methods=['POST'])
def proxy_api():
    """
    Proxy API requests to the backend and enhance the responses
    
    This provides a single endpoint to replace the direct API calls.
    Can return either regular JSON or a character-by-character stream.
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        # Prepare the API request
        query = data.get('message')
        if not query:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # Check cache first
        cached_response = get_cached_response(query)
        if cached_response:
            # If streaming is requested and we have a cached response
            if data.get('stream', False):
                @stream_with_context
                def generate_cached():
                    response_text = cached_response.get('response', '')
                    for char in response_text:
                        yield char
                        time.sleep(0.005)
                return Response(generate_cached(), content_type='text/plain')
            
            # Return cached response with cache indicator
            cached_response['cached'] = True
            return cached_response
        
        # Check if streaming is requested
        stream_mode = data.get('stream', False)
        logger.info(f"Proxying API request for query: {query} (stream={stream_mode})")
        
        # Build full URL
        url = urljoin(API_URL, API_ENDPOINT)
        
        # Remove stream parameter from data sent to API
        api_data = {k: v for k, v in data.items() if k != 'stream'}
        
        # Send the request to the backend API
        try:
            response = requests.post(
                url,
                json=api_data,
                headers={"Content-Type": "application/json"},
                timeout=60  # Increased timeout to 60 seconds
            )
            
            # Check response status
            if response.status_code != 200:
                logger.error(f"API request failed with status {response.status_code}")
                # Try direct Ollama API as fallback
                direct_response = _try_direct_ollama_api(query)
                if direct_response:
                    return jsonify({
                        'success': True,
                        'response': direct_response,
                        'source': 'direct_ollama_fallback'
                    })
                return jsonify({
                    'success': False,
                    'error': f"API request failed with status {response.status_code}",
                    'fallback': True,
                    'message': "Due to a backend issue, I couldn't process your request. Please try using the direct chat interface instead."
                }), 200  # Return 200 with error message for frontend
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            # Try direct Ollama API as fallback
            direct_response = _try_direct_ollama_api(query)
            if direct_response:
                return jsonify({
                    'success': True,
                    'response': direct_response,
                    'source': 'direct_ollama_fallback'
                })
            return jsonify({
                'success': False,
                'error': "API request timed out after 60 seconds",
                'fallback': True,
                'message': "The request took too long to process. Please try using the direct chat interface instead."
            }), 200
        except Exception as e:
            logger.error(f"Exception making API request: {str(e)}")
            # Try direct Ollama API as fallback
            direct_response = _try_direct_ollama_api(query)
            if direct_response:
                return jsonify({
                    'success': True,
                    'response': direct_response,
                    'source': 'direct_ollama_fallback'
                })
            return jsonify({
                'success': False,
                'error': f"Error connecting to API: {str(e)}",
                'fallback': True,
                'message': "I'm currently having trouble connecting to the backend systems. Please try using the direct chat interface instead."
            }), 200  # Return 200 with error message for frontend
        
        # Parse the API response
        api_response = response.json()
        
        # Extract the original response text
        original_text = None
        if 'response' in api_response:
            original_text = api_response['response']
        elif 'message' in api_response and isinstance(api_response['message'], str):
            original_text = api_response['message']
        elif 'message' in api_response and isinstance(api_response['message'], dict) and 'content' in api_response['message']:
            original_text = api_response['message']['content']
        
        # If no text found, return the original response
        if not original_text:
            logger.warning("Could not extract response text from API response")
            # If streaming, we need to decide what to stream. For now, let's assume api_response is json serializable for non-stream.
            # If it's an error or unexpected format from web service, this will pass it through.
            if stream_mode:
                 @stream_with_context
                 def generate_passthrough():
                    try:
                        # Attempt to stream the raw response if it's text-like
                        # This part is tricky as we don't know the exact format of original_text if it failed extraction
                        # For now, let's assume api_response itself might be the error message or a simple string.
                        # A more robust solution would depend on web service's error response format.
                        error_stream_content = json.dumps(api_response) # Default to streaming JSON of the error/full response
                        if isinstance(api_response, str):
                            error_stream_content = api_response

                        for char in error_stream_content:
                            yield char
                            time.sleep(0.005)
                    except Exception as stream_err:
                        logger.error(f"Error during passthrough stream generation: {stream_err}")
                        yield "Error generating stream response."
                 return Response(generate_passthrough(), content_type='text/plain')
            return jsonify(api_response) # Pass through the original JSON response
        
        # Enhance the response with RAG
        # enhanced_text = enhance_response(query, original_text) # DISABLED
        final_text = original_text # Use original_text directly
        
        # Determine if enhancement was applied
        # was_enhanced = enhanced_text != original_text # DISABLED
        was_enhanced = api_response.get('metadata', {}).get('rag_enhanced', False) # Check if web service marked it as RAG enhanced
        
        # Update the text to be returned (original or enhanced)
        # final_text = enhanced_text if was_enhanced else original_text # Already set to original_text
        
        # If streaming is requested, return a streaming response
        if stream_mode:
            logger.info("Streaming response for client")
            
            @stream_with_context
            def generate():
                # Stream the response character by character with a small delay
                for char in final_text:
                    yield char
                    # Small delay between characters (adjust as needed for desired speed)
                    time.sleep(0.005)  # 5ms delay 
            
            return Response(generate(), content_type='text/plain')
        
        # Otherwise, update the API response with the enhanced text and return as JSON
        # if was_enhanced: # Logic for adding 'rag_enhanced' metadata is now responsibility of web service
        #     logger.info("Response was enhanced with RAG")
        #     if 'response' in api_response:
        #         api_response['response'] = final_text 
        #     elif 'message' in api_response and isinstance(api_response['message'], str):
        #         api_response['message'] = final_text
        #     elif 'message' in api_response and isinstance(api_response['message'], dict) and 'content' in api_response['message']:
        #         api_response['message']['content'] = final_text
            
        #     # Add RAG metadata
        #     if 'metadata' not in api_response:
        #         api_response['metadata'] = {}
        #     api_response['metadata']['rag_enhanced'] = True
        
        # Cache the successful response before returning
        # The api_response from web service is cached directly.
        # If web service indicates RAG enhancement, that's part of the cached response.
        cache_response(query, api_response)
        
        return jsonify(api_response) # Return the original api_response from web service
        
    except Exception as e:
        logger.error(f"Error proxying API request: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Get port from command-line arguments or environment variable, default to 5000
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.warning(f"Invalid port provided as argument: {sys.argv[1]}. Using default {port}.")
    else:
        port_env = os.environ.get('PORT')
        if port_env:
            try:
                port = int(port_env)
            except ValueError:
                logger.warning(f"Invalid port in ENV: {port_env}. Using default {port}.")
    
    logger.info(f"Starting RAG Web Connector on port {port}")
    app.run(host='0.0.0.0', port=port) 