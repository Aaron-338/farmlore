# core/views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
        data = json.loads(request.body)
        messages = data.get('messages', [])
        
        if not messages:
            return JsonResponse({'error': 'No messages provided'})
        
        # Get the last user message
        last_user_message = None
        for message in reversed(messages):
            if message['role'] == 'user':
                last_user_message = message['content']
                break
        
        if not last_user_message:
            return JsonResponse({'error': 'No user message found'})
        
        # For now, return a simple response
        return JsonResponse({
            'message': {
                'role': 'assistant',
                'content': 'I processed your question. If I had more specific information in my knowledge base, I would share it with you.'
            }
        })
    
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
