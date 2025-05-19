import json
import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

# Import the prompt type detection function
from api.inference_engine.prompt_templates import detect_prompt_type



# Set up logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)



# Attempt to import PrologEngine carefully

PROLOG_ENGINE_INSTANCE = None

PROLOG_ENGINE_INIT_ERROR = None



try:

    # from api.inference_engine.prolog_engine import PrologEngine # Old import
    from api.inference_engine.hybrid_engine import HybridEngine # New import

    # We will instantiate it per request or on first use, not globally here

    PROLOG_ENGINE_AVAILABLE = True # Assuming HybridEngine is the way forward

    logger.info("HybridEngine class imported successfully.")

except ImportError as e:

    PROLOG_ENGINE_AVAILABLE = False

    PROLOG_ENGINE_INIT_ERROR = f"Failed to import HybridEngine: {str(e)}"

    logger.error(PROLOG_ENGINE_INIT_ERROR + " Chat API will have limited functionality.")

    class HybridEngine: # Stub class if import fails, to prevent further crashes

        def __init__(self):

            logger.warning("Using stub HybridEngine due to import failure.")

        def query(self, query_type, params):

            logger.warning("HybridEngine (stub) not available. Returning stubbed response.")

            return {"response": "HybridEngine (stub) not available. This is a stubbed response.", "source": "stub", "success": False}



def get_prolog_engine():

    """Lazily instantiates and returns the HybridEngine."""

    global PROLOG_ENGINE_INSTANCE, PROLOG_ENGINE_INIT_ERROR, PROLOG_ENGINE_AVAILABLE



    if not PROLOG_ENGINE_AVAILABLE:

        return HybridEngine() # Return a new stub instance



    if PROLOG_ENGINE_INSTANCE is None and PROLOG_ENGINE_INIT_ERROR is None:

        try:

            logger.info("Attempting to instantiate HybridEngine for the first time...")

            PROLOG_ENGINE_INSTANCE = HybridEngine()

            logger.info("HybridEngine instantiated successfully.")

        except Exception as e:

            PROLOG_ENGINE_INIT_ERROR = f"Error instantiating HybridEngine: {str(e)}"

            logger.error(PROLOG_ENGINE_INIT_ERROR + " Chat API may not function correctly.")

            PROLOG_ENGINE_INSTANCE = HybridEngine() # Fallback to stub

    

    if PROLOG_ENGINE_INIT_ERROR and not isinstance(PROLOG_ENGINE_INSTANCE, HybridEngine):

        return HybridEngine()



    return PROLOG_ENGINE_INSTANCE



@api_view(['POST'])

@permission_classes([AllowAny])

def chat_api(request):

    """Handle chat messages using HybridEngine."""

    logger.info("==== CHAT API CALLED (using HybridEngine) ====")

    

    engine = get_prolog_engine() # Gets HybridEngine instance or its stub



    # Check if the engine is a stub due to import or instantiation failure

    if PROLOG_ENGINE_INIT_ERROR or not PROLOG_ENGINE_AVAILABLE:

        error_message = PROLOG_ENGINE_INIT_ERROR or "HybridEngine could not be imported."

        logger.error(f"HybridEngine not available: {error_message}. Returning error response.")

        return Response({

            'error': f"Core processing engine failed: {error_message}",

            'success': False,

            'source': 'error_hybrid_engine_failure'

        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    try:

        message = request.data.get('message')

        if not message:

            logger.warning("No message provided in the request.")

            return Response({

                'error': 'No message provided',

                'success': False,

                'source': 'error_no_message'

            }, status=status.HTTP_400_BAD_REQUEST)



        logger.info(f"Received message for HybridEngine: {message}")

        # Dynamically determine the query type based on the message content
        prompt_type = detect_prompt_type(message)
        query_type = prompt_type.value if hasattr(prompt_type, 'value') else 'general_query'
        
        logger.info(f"Detected query type: {query_type} for message: {message[:50]}...")

        # Call HybridEngine.query() with the detected query_type and params
        # The HybridEngine.query expects params to be a dict.
        engine_params = {"query": message, "message": message} # Pass message for both for now

        engine_response = engine.query(query_type=query_type, params=engine_params)
        
        logger.info(f"Response from HybridEngine: {engine_response}")



        # HybridEngine.query is expected to return a dictionary.

        if engine_response and isinstance(engine_response, dict):

            final_response_data = engine_response

            # Ensure 'success' key, default to True if response seems okay and no error key

            if 'success' not in final_response_data and 'error' not in final_response_data:

                final_response_data['success'] = True

            elif 'error' in final_response_data and 'success' not in final_response_data:

                 final_response_data['success'] = False # ensure success is false if error is present

        else:

            logger.warning("HybridEngine returned an invalid response format.")

            final_response_data = {

                'response': 'Could not get a valid response from the processing engine.',

                'success': False,

                'source': 'error_engine_invalid_response_format'

            }

        

        return Response(final_response_data)



    except Exception as e:

        logger.error(f"Error in chat_api while processing with HybridEngine: {str(e)}")

        logger.exception("Exception details:") # Logs full traceback

        return Response({

            'error': f"An internal error occurred: {str(e)}",

            'success': False,

            'source': 'error_chat_api_exception'

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

class TrainedModelViewSet(ViewSet):

    """Minimal stub for TrainedModelViewSet, now inheriting from DRF ViewSet"""

    # Routers often expect a 'list' action for the root of the viewset.
    def list(self, request):
        return Response({"message": "TrainedModelViewSet stub - list action"})


class HybridEngineView(APIView):

    """Simplified HybridEngineView."""

    def post(self, request, format=None):

        return Response({"success": True, "result": {"response": "Simplified hybrid engine response"}})


class EngineStatsView(APIView):

    """Returns the current statistics and status of the inference engines."""

    def get(self, request, format=None):
        logger.info("EngineStatsView: GET request received")
        try:
            engine = get_prolog_engine() # Get the HybridEngine instance
            
            if PROLOG_ENGINE_INIT_ERROR or not PROLOG_ENGINE_AVAILABLE or isinstance(engine, type) and engine.__name__ == 'HybridEngine' and not hasattr(engine, 'get_stats'):
                error_detail = PROLOG_ENGINE_INIT_ERROR or "HybridEngine not properly initialized."
                logger.warning(f"EngineStatsView: HybridEngine not available or is a stub. Detail: {error_detail}")
                return Response({
                    "success": True,
                    "stats": {
                        "ollama_available": False,
                        "ollama_initialized": True,
                        "prolog_available": PROLOG_ENGINE_AVAILABLE,
                        "status_message": f"HybridEngine issue: {error_detail}",
                        "error": "Engine not fully operational"
                    }
                }, status=status.HTTP_200_OK)

            engine_stats = engine.get_stats()
            logger.info(f"EngineStatsView: Successfully retrieved stats from HybridEngine: {engine_stats}")
            
            ollama_stats = engine_stats.get("ollama_handler_stats", {})
            prolog_stats = engine_stats.get("prolog_service_stats", {})

            ollama_configured = ollama_stats.get("configured", False)
            ollama_init_pending = ollama_stats.get("initialization_pending", True)
            ollama_init_successful = ollama_stats.get("initialization_successful", False)
            
            frontend_ollama_initialized = ollama_configured and not ollama_init_pending

            frontend_ollama_available = frontend_ollama_initialized and ollama_init_successful and ollama_stats.get("available", False)

            formatted_stats = {
                "ollama_available": frontend_ollama_available,
                "ollama_initialized": frontend_ollama_initialized,
                "prolog_available": prolog_stats.get("available", PROLOG_ENGINE_AVAILABLE),
                "details": engine_stats
            }
            
            return Response({
                "success": True,
                "stats": formatted_stats
            })

        except Exception as e:
            logger.error(f"EngineStatsView: Error getting engine stats: {str(e)}", exc_info=True)
            return Response({
                "success": False,
                "error": "Failed to retrieve engine statistics",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

