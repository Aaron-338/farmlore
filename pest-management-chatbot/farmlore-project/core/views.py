# core/views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import logging

# Import PrologEngine
from api.inference_engine.prolog_engine import PrologEngine

# It might be more performant to initialize PrologEngine once globally or per worker
# For simplicity here, we'll instantiate it per request, but consider this for optimization.
# prolog_engine_instance = PrologEngine() # Example of a global instance

def home_view(request):
    """
    Landing page view that presents the two main pathways:
    - Community Platform
    - FarmLore Chatbot
    """
    # Show the landing page with pathway options
    return render(request, 'landing_page.html')

def about_view(request):
    """About page view"""
    return render(request, 'about.html')

def chat(request):
    """Chat page view"""
    return render(request, 'core/chat.html')

def chat_api(request):
    """API endpoint for the chat interface"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            messages = data.get('messages', [])
            
            if not messages:
                return JsonResponse({'error': 'No messages provided'}, status=400)
            
            last_user_message_content = None
            for message in reversed(messages):
                if message.get('role') == 'user':
                    last_user_message_content = message.get('content')
                    break
            
            if not last_user_message_content:
                return JsonResponse({'error': 'No user message found'}, status=400)

            engine = PrologEngine() 

            engine_response_list = engine.query(last_user_message_content)

            if engine_response_list and isinstance(engine_response_list, list) and len(engine_response_list) > 0:
                first_result = engine_response_list[0]
                if isinstance(first_result, dict):
                    assistant_reply = first_result.get('response', "Sorry, I encountered an issue processing your request.")
                    response_source = first_result.get('source', 'unknown')
                    # Ensure logging is imported to use logging.info
                    logging.info(f"Chat API: User query '{last_user_message_content}', Engine source: '{response_source}'")
                else:
                    assistant_reply = "Sorry, the response from the engine was not in the expected format."
                    logging.warning(f"Chat API: Unexpected response format from engine: {first_result}")
            else:
                assistant_reply = "Sorry, I couldn't get a response from the engine."
                logging.error(f"Chat API: Empty or invalid response from engine: {engine_response_list}")

            return JsonResponse({
                'message': {
                    'role': 'assistant',
                    'content': assistant_reply
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            logging.error(f"Chat API error: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'An unexpected error occurred on the server.'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def prolog_query_api(request):
    """API endpoint for direct Prolog queries"""
    if request.method == 'POST':
        data = json.loads(request.body)
        query_type = data.get('query_type')
        
        # For now, return a placeholder response
        if query_type == 'pest_solutions':
            pest = data.get('pest')
            region = data.get('region', 'global')
            return JsonResponse({'solutions': []})
        
        elif query_type == 'recommend':
            pest = data.get('pest')
            return JsonResponse({'recommendation': None})
        
        elif query_type == 'pest_info':
            pest = data.get('pest')
            return JsonResponse({'info': None})
        
        return JsonResponse({'error': 'Invalid query type'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
