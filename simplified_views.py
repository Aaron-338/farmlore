import json
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_api(request):
    """Handle chat messages with hardcoded response for testing."""
    try:
        # Log that we were called
        logger.info("==== CHAT API CALLED - USING SIMPLIFIED DIRECT RESPONSE ====")
        
        # Extract the message if possible, but it doesn't matter for our test
        try:
            message = request.data.get('message', 'No message provided')
            logger.info(f"Received message: {message}")
        except:
            message = "Could not parse message"
            logger.info("Could not parse message from request")

        # Return a hardcoded response for testing
        test_response = "DIRECT RESPONSE: This is a test response from the simplified views.py that bypasses all dependencies."
        response_data = {
            'response': test_response,
            'source': 'direct_test',
            'success': True
        }
            
        return Response(response_data)
    except Exception as e:
        logger.error(f"Error in simplified chat_api: {str(e)}")
        return Response({
            'error': f"Error in simplified chat_api: {str(e)}",
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Adding a minimal set of required functions from the original views.py
# to make the URL routing work

@api_view(['POST'])
def predict(request):
    """Simplified predict endpoint."""
    return Response({"message": "Simplified predict endpoint"})

@api_view(['GET'])
def available_values(request):
    """Simplified available values endpoint."""
    return Response({"message": "Simplified available values endpoint"})

@api_view(['POST'])
def search_pests(request):
    """Simplified search pests endpoint."""
    return Response({"message": "Simplified search pests endpoint"})

@api_view(['POST'])
def search_methods(request):
    """Simplified search methods endpoint."""
    return Response({"message": "Simplified search methods endpoint"})

@api_view(['POST'])
def search_soil(request):
    """Simplified search soil endpoint."""
    return Response({"message": "Simplified search soil endpoint"})

@api_view(['POST'])
def feedback_api(request):
    """Simplified feedback endpoint."""
    return Response({"message": "Simplified feedback endpoint"})

@api_view(['GET'])
def health_check(request):
    """Simplified health check endpoint."""
    return Response({"status": "healthy"})

@api_view(['GET'])
def model_health(request):
    """Simplified model health endpoint."""
    return Response({"status": "healthy"})

@api_view(['GET'])
def test_models(request):
    """Simplified test models endpoint."""
    return Response({"status": "success"})

@api_view(['GET'])
def debug_hybrid_engine(request):
    """Simplified debug hybrid engine endpoint."""
    return Response({"success": True})

@api_view(['POST'])
def chat_with_ai(request):
    """Simplified chat with AI endpoint."""
    return Response({"success": True, "response": "Simplified chat with AI endpoint"})

@api_view(['GET'])
def test_endpoint(request):
    """Simplified test endpoint."""
    return Response({"message": "Test endpoint is working correctly", "success": True})

# Creating minimal class-based views required by urls.py
from rest_framework.views import APIView

class DatasetViewSet:
    """Minimal stub for DatasetViewSet"""
    @classmethod
    def as_view(cls, actions=None):
        return lambda request: JsonResponse({"message": "DatasetViewSet stub"})

class TrainedModelViewSet:
    """Minimal stub for TrainedModelViewSet"""
    @classmethod
    def as_view(cls, actions=None):
        return lambda request: JsonResponse({"message": "TrainedModelViewSet stub"})

class HybridEngineView(APIView):
    """Simplified HybridEngineView."""
    def post(self, request, format=None):
        return Response({"success": True, "result": {"response": "Simplified hybrid engine response"}})

class EngineStatsView(APIView):
    """Simplified EngineStatsView."""
    def get(self, request, format=None):
        return Response({"success": True, "stats": {"status": "ok"}})
