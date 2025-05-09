from django.shortcuts import render
from django.http import JsonResponse
import json
import logging
import re
from api.inference_engine.hybrid_engine import HybridEngine
from api.inference_engine.prompt_templates import detect_prompt_type

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize the hybrid engine
hybrid_engine = HybridEngine()

def home(request):
    """Home page view"""
    return render(request, 'chatbot/home.html')

def chat(request):
    """Chat interface view"""
    return render(request, 'chatbot/chat.html')

def about(request):
    """About page view"""
    return render(request, 'chatbot/about.html')

def detect_query_type(query):
    """
    Detect the query type based on its content
    """
    query_lower = query.lower()
    
    # Check for pest identification
    if any(term in query_lower for term in ["identify", "what pest", "what insect", "what disease"]):
        return "pest_identification"
    
    # Check for control methods
    if any(term in query_lower for term in ["control", "manage", "treat", "get rid of", "solution"]):
        return "control_methods"
    
    # Check for crop pests
    if any(term in query_lower for term in ["crops affected", "what crops", "crop pests"]):
        return "crop_pests"
    
    # Check for indigenous knowledge
    if any(term in query_lower for term in ["traditional", "indigenous", "old methods"]):
        return "indigenous_knowledge"
    
    # Default to general query
    return "general_query"

def extract_entities(query):
    """
    Extract entities like crop names, pest names, etc. from the query
    """
    params = {}
    
    # Extract crop names
    crop_pattern = r"(?:crop|plant|harvest|grow|farming|crops|plants|vegetables|fruits).*?\b(maize|corn|wheat|tomato|potato|beans|rice|sorghum|millet|apple|banana|carrot|onion|garlic|cabbage|lettuce)\b"
    crop_match = re.search(crop_pattern, query.lower())
    if crop_match:
        params["crop"] = crop_match.group(1)
    
    # Extract pest names
    pest_pattern = r"\b(aphid|thrips|whitefly|armyworm|caterpillar|beetle|weevil|mite|nematode|cutworm|bollworm|grasshopper|locust|mealybug|scale insect)\b"
    pest_match = re.search(pest_pattern, query.lower())
    if pest_match:
        params["pest"] = pest_match.group(1)
    
    # Extract symptoms
    symptom_pattern = r"\b(wilting|yellowing|stunted|holes|spots|curling|discoloration|mold|rot|blight|mosaic|virus|bacterial|fungal)\b"
    symptom_matches = re.findall(symptom_pattern, query.lower())
    if symptom_matches:
        params["symptoms"] = symptom_matches
    
    return params

def chat_api(request):
    """API endpoint for chat interface"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Handle different message formats
            message = None
            if 'messages' in data and isinstance(data['messages'], list):
                for msg in reversed(data['messages']):
                    if isinstance(msg, dict) and msg.get('role') == 'user':
                        message = msg.get('content')
                        break
                if not message and data['messages']:
                    message = data['messages'][-1].get('content', '') if isinstance(data['messages'][-1], dict) else data['messages'][-1]
            elif 'message' in data:
                message = data.get('message')
            
            if not message:
                return JsonResponse({
                    'success': False,
                    'error': 'No message provided',
                    'message': {
                        'role': 'assistant',
                        'content': 'Sorry, I could not process your request. No message was provided.'
                    }
                })
            
            # Detect query type and extract entities
            query_type = detect_query_type(message)
            params = extract_entities(message)
            params['query'] = message
            
            # Log the processing details
            logger.info(f"Processing query: '{message}', type: {query_type}, params: {params}")
            
            # Process the query using the hybrid engine
            result = hybrid_engine.query(query_type, params)
            
            # Determine source based on the result
            source = None
            if 'source' in result:
                # Map source from hybrid_engine to our frontend terminology
                source_mapping = {
                    'ollama': 'llm',
                    'prolog': 'prolog',
                    'hybrid': 'llm',  # If hybrid, show as LLM since it used Ollama
                    'cache': 'llm',   # If from cache, it was originally from LLM
                    'mock': 'prolog'  # If mock data, it's rule-based
                }
                source = source_mapping.get(result['source'], 'prolog')
            
            # Determine if the Ollama service is initialized
            is_initialized = hybrid_engine.is_initialization_complete()[0]
            
            # Return the response with consistent metadata
            return JsonResponse({
                'success': True,
                'message': {
                    'role': 'assistant',
                    'content': result.get('response', 'I could not generate a response. Please try again.')
                },
                'metadata': {
                    'query_type': query_type,
                    'detected_entities': params,
                    'source': source,
                    'engine_status': {
                        'ollama_initialized': is_initialized,
                        'ollama_available': hybrid_engine.use_ollama and hybrid_engine.ollama_handler.is_available if hybrid_engine.use_ollama else False
                    }
                },
                'source': source  # Include at the top level for backward compatibility
            })
        except Exception as e:
            import traceback
            logger.error(f"Error in chat_api: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': {
                    'role': 'assistant',
                    'content': 'Sorry, I encountered a technical issue while processing your request. Please try again.'
                },
                'source': 'prolog',  # Default to prolog for error messages
                'error_details': traceback.format_exc()
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method',
        'message': {
            'role': 'assistant',
            'content': 'This endpoint only accepts POST requests.'
        },
        'source': 'prolog'  # Default to prolog for error messages
    }, status=405)

def prolog_query_api(request):
    """API endpoint for Prolog queries"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query_type = data.get('query_type')
            
            if not query_type:
                return JsonResponse({
                    'success': False,
                    'error': 'No query_type provided',
                    'message': {
                        'role': 'assistant',
                        'content': 'Query type must be specified.'
                    }
                }, status=400)
            
            params = {}
            
            # Extract parameters based on query type
            if query_type == 'pest_solutions':
                params['pest'] = data.get('pest')
                params['region'] = data.get('region', 'Lesotho')
                
            elif query_type == 'recommend':
                params['pest'] = data.get('pest')
                
            elif query_type == 'pest_info':
                params['pest'] = data.get('pest')
            
            # Process the query using the hybrid engine
            result = hybrid_engine.query(query_type, params)
            
            return JsonResponse({
                'success': True,
                'result': result
            })
            
        except Exception as e:
            import traceback
            logger.error(f"Error in prolog_query_api: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': {
                    'role': 'assistant',
                    'content': 'Sorry, I encountered a technical issue while processing your request. Please try again.'
                },
                'error_details': traceback.format_exc()
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method',
        'message': {
            'role': 'assistant',
            'content': 'This endpoint only accepts POST requests.'
        }
    }, status=405)
