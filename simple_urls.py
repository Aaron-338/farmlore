from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Simple test view that doesn't require any imports
@csrf_exempt
def simple_chat_api(request):
    from rest_framework.response import Response
    from django.http import JsonResponse
    return JsonResponse({
        'response': 'This is a direct response from the simplified chat API handler',
        'source': 'direct_simple',
        'success': True
    })

urlpatterns = [
    path('chat/', simple_chat_api, name='chat-api-simple'),
] 