import json
import logging
import re
from difflib import SequenceMatcher
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import (
    PredictionRequestSerializer,
    PestQuerySerializer,
    SoilQuerySerializer,
    DatasetSerializer,
    TrainedModelSerializer
)
from .models import Dataset, TrainedModel
from .mock_data import filter_pests, filter_methods, filter_soil
from .inference_engine.hybrid_engine import HybridEngine
from django.conf import settings
from .response_patterns import RESPONSE_PATTERNS, INTENT_RESPONSES, INTENT_KEYWORDS
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from api.chat_logger import start_chat_tracking, log_chat_step, end_chat_tracking

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the hybrid engine
engine = HybridEngine()

# Initialize the hybrid engine as a singleton
hybrid_engine = HybridEngine()

class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing dataset entries."""
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class TrainedModelViewSet(viewsets.ModelViewSet):
    """ViewSet for managing trained models."""
    queryset = TrainedModel.objects.all()
    serializer_class = TrainedModelSerializer

@api_view(['POST'])
def predict(request):
    """Predict pest control method based on crop and symptoms."""
    serializer = PredictionRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Mock response
    result = {
        "prediction": "Organic Pesticide",
        "confidence": 0.85,
        "alternatives": [
            {"method": "Organic Pesticide", "probability": 0.85},
            {"method": "Biological Control", "probability": 0.10},
            {"method": "Cultural Control", "probability": 0.05}
        ]
    }
    
    return Response(result)

@api_view(['GET'])
def available_values(request):
    """Get available values for input features."""
    # Mock response
    values = {
        "host_crops": ["Rice", "Corn", "Tomato", "Cabbage", "Potato"],
        "early_symptoms": ["Yellow leaves", "Wilting", "Spots", "Holes", "Dark spots", "Curled leaves", "Defoliation"],
        "advanced_symptoms": ["Dead leaves", "Stunted growth", "Damaged ears", "Severe defoliation", "Rotting tubers"],
        "methods": ["Organic Pesticide", "Biological Control", "Cultural Control", "Mechanical Control", "Resistant Varieties"]
    }
    
    return Response(values)

@api_view(['POST'])
def search_pests(request):
    """Search for pests by name or symptoms."""
    serializer = PestQuerySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    query = serializer.validated_data['query']
    results = filter_pests(query)
    
    return Response(results)

@api_view(['POST'])
def search_methods(request):
    """Search for control methods by pest ID."""
    pest_id = request.data.get('pest_id', '')
    results = filter_methods(pest_id)
    
    return Response(results)


@api_view(['POST'])
def search_soil(request):
    """Search for soil treatments by soil type or crop."""
    serializer = SoilQuerySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    soil_type = serializer.validated_data.get('soil_type', '')
    crop = serializer.validated_data.get('crop', '')
    
    results = filter_soil(soil_type, crop)
    
    return Response(results)

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_api(request):
    """Handle chat messages using pattern matching."""
    try:
        # Parse request data
        logger.info("================ CHAT API CALLED ================")
        data = request.data
        
        # Log the raw request data for debugging
        logger.info(f"Raw request data: {data}")
        
        # Check if the message is in the expected format or in a nested structure
        message = None
        
        if 'message' in data:
            message = data.get('message', '').strip()
            logger.info(f"Found message in 'message' field: {message}")
        elif 'messages' in data and isinstance(data['messages'], list):
            # First try to find the user message in the array
            user_message = None
            for msg in data['messages']:
                if isinstance(msg, dict) and msg.get('role') == 'user' and 'content' in msg:
                    user_message = msg.get('content', '').strip()
                    logger.info(f"Found user message in messages array: {user_message}")
                    break
            
            if user_message:
                message = user_message
            # If no user message found, fall back to the first message
            elif len(data['messages']) > 0:
                msg_obj = data['messages'][0]
                if isinstance(msg_obj, dict):
                    if 'content' in msg_obj:
                        message = msg_obj.get('content', '').strip()
                        logger.info(f"Falling back to messages[0].content field: {message}")
                    elif 'message' in msg_obj:
                        message = msg_obj.get('message', '').strip()
                        logger.info(f"Falling back to messages[0].message field: {message}")
                elif isinstance(msg_obj, str):
                    message = msg_obj.strip()
                    logger.info(f"Falling back to string in messages[0]: {message}")
        elif isinstance(data, str):
            # Handle case where entire request body is the message
            message = data.strip()
            logger.info(f"Request body is the message: {message}")
        
        if not message:
            logger.error("Could not extract message from request")
            return Response({
                'error': 'No message could be extracted from the request',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Start tracking the chat message
        message_id = start_chat_tracking(query=message)
        log_chat_step(message_id, "API RECEIVED", f"Message length: {len(message)}")
        
        # Process the message using pattern matching
        logger.info(f"PROCESSING QUERY: '{message}'")
        message_lower = message.lower()
        
        # First try to match against our predefined patterns
        log_chat_step(message_id, "API PATTERN MATCHING", "Checking for pattern matches")
        
        # Define patterns and responses
        patterns = [
            {
                'keywords': ['tomato', 'pest'],
                'name': 'tomato_pests',
                'response': "Common pests affecting tomatoes include tomato hornworms, aphids, whiteflies, spider mites, thrips, and cutworms. These pests can damage leaves, stems, and fruits. Regular inspection and integrated pest management helps prevent severe damage."
            },
            {
                'keywords': ['cabbage', 'aphid'],
                'name': 'cabbage_aphids',
                'response': "To control aphids on cabbage: 1) Use insecticidal soap or neem oil spray, 2) Introduce beneficial insects like ladybugs, 3) Use a strong water spray to dislodge them, 4) Apply diatomaceous earth around plants, and 5) For severe infestations, consider organic pyrethrins. Regularly check the undersides of leaves where aphids often hide."
            },
            {
                'keywords': ['rice', 'yellow'],
                'name': 'rice_yellow_leaves',
                'response': "Yellow leaves in rice plants often indicate nutrient deficiency, particularly nitrogen. They could also be a sign of diseases like Rice Yellow Mottle Virus, bacterial leaf blight, or pest infestations like leafhoppers. Examine the pattern of yellowing - if older leaves yellow first, it's likely nitrogen deficiency. If new leaves yellow, it might be iron or zinc deficiency. Check also for water management issues."
            },
            {
                'keywords': ['soil', 'fertil'],
                'name': 'soil_fertilization',
                'response': "Natural methods for soil fertilization include: 1) Composting kitchen scraps and yard waste, 2) Using cover crops like legumes to fix nitrogen, 3) Applying well-rotted manure, 4) Making compost tea, 5) Adding worm castings, and 6) Utilizing green manures. These methods improve soil structure, add nutrients gradually, and promote beneficial soil organisms."
            },
            {
                'keywords': ['rice', 'pest'],
                'name': 'rice_pests',
                'response': "Common rice pests include: 1) Rice stem borers - causing deadhearts and whiteheads, 2) Rice leafhoppers and planthoppers - transmitting viral diseases, 3) Rice water weevil - damaging roots, 4) Rice gall midge - creating galls on developing tillers, and 5) Armyworms - feeding on foliage. Integrated pest management combining resistant varieties, cultural practices, and judicious pesticide use works best."
            }
        ]
        
        # Check patterns
        matched_response = None
        for pattern in patterns:
            # If all keywords are in the message, use this pattern's response
            keywords_present = all(keyword in message_lower for keyword in pattern['keywords'])
            if keywords_present:
                matched_response = pattern['response']
                log_chat_step(message_id, "API MATCH FOUND", f"Pattern: {pattern['name']}")
                break
        
        # If we matched a pattern, return it
        if matched_response:
            log_chat_step(message_id, "API PATTERN RESPONSE", "Using predefined pattern response")
            response_data = {
                'response': matched_response,
                'source': 'pattern',
                'success': True
            }
            end_chat_tracking(message_id, matched_response, 'pattern')
            return Response(response_data)
        
        # No pattern match, try using the hybrid engine
        log_chat_step(message_id, "API USING ENGINE", "Sending to hybrid engine")
        
        try:
            # Pass to the hybrid engine
            result = hybrid_engine.query("general_query", {"query": message})
            log_chat_step(message_id, "ENGINE PROCESSING COMPLETE", f"Source: {result.get('source', 'unknown')}")
            
            if "response" in result and result["response"]:
                response = result["response"]
                source = result.get("source", "hybrid_engine")
                
                response_data = {
                    'response': response,
                    'source': source,
                    'success': True
                }
                
                end_chat_tracking(message_id, response, source)
                return Response(response_data)
            else:
                log_chat_step(message_id, "ENGINE NO RESPONSE", "Engine returned no response")
        except Exception as e:
            log_chat_step(message_id, "ENGINE ERROR", str(e))
            logger.error(f"Error from hybrid engine: {str(e)}")
            # Fall through to default response
        
        # If all else fails, provide a default response
        default_response = (
            "I'm sorry, but I couldn't find specific information about that. "
            "Please try asking about common pests, treatment methods, or sustainable farming practices."
        )
        
        log_chat_step(message_id, "API DEFAULT RESPONSE", "Using default fallback response")
        response_data = {
            'response': default_response,
            'source': 'default',
            'success': True
        }
        
        end_chat_tracking(message_id, default_response, 'default')
        return Response(response_data)
    except Exception as e:
        logger.error(f"Unhandled exception in chat_api: {str(e)}")
        return Response({
            'error': f"An error occurred while processing your request: {str(e)}",
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HybridEngineView(APIView):
    """
    API endpoint for interacting with the HybridEngine
    """
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, format=None):
        """
        Process a query using the HybridEngine
        
        Accepts:
        {
            "query_type": "pest_identification|control_methods|crop_pests|indigenous_knowledge|general_query",
            "query": "User's natural language query",
            "params": {
                // Additional parameters specific to the query type
            }
        }
        """
        try:
            # Extract data from request
            query_type = request.data.get('query_type', 'general_query')
            query = request.data.get('query', '')
            params = request.data.get('params', {})
            
            # Add the query to params if provided
            if query:
                params['query'] = query
                
            # Log the request
            logger.info(f"Received request - Type: {query_type}, Query: {query[:50]}{'...' if len(query) > 50 else ''}")
            
            # Check if Ollama initialization is complete with a short timeout
            is_complete, is_successful = hybrid_engine.is_initialization_complete(timeout=0.1)
            if not is_complete:
                logger.info("Ollama is still initializing. Using Prolog fallback for now.")
                # Force use_ollama to False temporarily for this request
                original_use_ollama = hybrid_engine.use_ollama
                hybrid_engine.use_ollama = False
                
                # Process the query with Prolog fallback
                result = hybrid_engine.query(query_type, params)
                
                # Restore original value
                hybrid_engine.use_ollama = original_use_ollama
                
                # Add initialization status to the response
                result['source'] = "prolog"
                result['initialization_status'] = "in_progress"
                
                # Add stats to the response
                result['stats'] = {
                    'query_count': hybrid_engine.query_count,
                    'cache_hit_rate': hybrid_engine.cache_hit_count / hybrid_engine.query_count if hybrid_engine.query_count > 0 else 0,
                    'engine_used': "prolog",
                    'ollama_status': "initializing"
                }
                
                # Return the result
                return Response({
                    'success': True,
                    'result': result
                })
            
            # Record the engine state before query
            using_ollama_before = hybrid_engine.use_ollama
            
            # Process the query
            result = hybrid_engine.query(query_type, params)
            
            # Determine which engine was used (check if use_ollama changed due to fallback)
            engine_used = "llm" if using_ollama_before and hybrid_engine.use_ollama else "prolog"
            
            # Add source information to the result
            result['source'] = engine_used
            
            # Add stats to the response
            result['stats'] = {
                'query_count': hybrid_engine.query_count,
                'cache_hit_rate': hybrid_engine.cache_hit_count / hybrid_engine.query_count if hybrid_engine.query_count > 0 else 0,
                'engine_used': engine_used
            }
            
            # Return the result
            return Response({
                'success': True,
                'result': result
            })
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            import traceback
            return Response({
                'success': False,
                'error': str(e),
                'message': 'An error occurred while processing your request',
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EngineStatsView(APIView):
    """API endpoint for retrieving engine statistics"""
    def get(self, request, format=None):
        try:
            stats = hybrid_engine.get_stats()
            return Response({
                'success': True,
                'stats': stats
            })
        except Exception as e:
            logger.error(f"Error retrieving stats: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def feedback_api(request):
    """Handle feedback on chat responses."""
    try:
        data = request.data
        logger.info(f"Received feedback: {data}")
        
        # Extract data
        message_id = data.get('message_id')
        feedback_type = data.get('feedback_type')
        message_content = data.get('message_content', '')
        message_source = data.get('message_source', 'unknown')
        
        if not message_id or not feedback_type:
            return Response({
                'success': False,
                'error': 'Missing required fields'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate feedback type
        if feedback_type not in ['positive', 'negative']:
            return Response({
                'success': False,
                'error': 'Invalid feedback type'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Store feedback in database
        from api.models import ResponseFeedback
        ResponseFeedback.objects.create(
            message_id=message_id,
            feedback_type=feedback_type,
            message_content=message_content,
            message_source=message_source,
            user=request.user if request.user.is_authenticated else None
        )
        
        logger.info(f"Feedback saved - ID: {message_id}, Type: {feedback_type}, Source: {message_source}")
        
        return Response({
            'success': True,
            'message': 'Feedback received'
        })
    
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)