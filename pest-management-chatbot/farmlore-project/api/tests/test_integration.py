"""Integration tests for the pest management chatbot."""
import json
import pytest
from django.test import AsyncClient
from django.urls import reverse
from rest_framework import status
from api.inference_engine.hybrid_engine import HybridEngine
from api.inference_engine.prolog_engine import PrologEngine
from api.inference_engine.llm_handler import OllamaHandler

pytestmark = pytest.mark.asyncio

from pytest_asyncio import fixture

@fixture
async def client():
    """Create an async test client."""
    client = AsyncClient()
    return client

@fixture
async def hybrid_engine():
    """Create a hybrid engine instance."""
    engine = HybridEngine()
    return engine

@pytest.fixture
def test_queries():
    """Sample test queries and expected results."""
    return [
        {
            "query": "How do I identify tomato hornworm?",
            "expected_intent": "pest_identification",
            "expected_entities": {"pest": "hornworm", "crop": "tomato"}
        },
        {
            "query": "What are good prevention methods for aphids in tomatoes?",
            "expected_intent": "prevention",
            "expected_entities": {"pest": "aphids", "crop": "tomato"}
        },
        {
            "query": "How can I control whiteflies on my tomato plants?",
            "expected_intent": "control_methods",
            "expected_entities": {"pest": "whiteflies", "crop": "tomato"}
        }
    ]

async def test_chat_api_endpoint(client, test_queries):
    """Test the chat API endpoint."""
    url = '/api/chat/'  # Direct URL path since we're testing
    
    for query in test_queries:
        # Test request
        payload = {
            "message": query["query"],
            "context": {}
        }
        
        response = await client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Verify response structure
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'success' in data
        assert data['success'] is True
        assert 'message' in data
        assert 'metadata' in data
        assert 'confidence' in data['metadata']
        assert 'prolog_data' in data['metadata']
        
        # Verify confidence score is reasonable
        assert 0 <= data['metadata']['confidence'] <= 1

async def test_hybrid_engine_query_analysis(hybrid_engine, test_queries):
    """Test the hybrid engine's query analysis capabilities."""
    for query in test_queries:
        # Test intent and entity extraction
        intent, entities = await hybrid_engine._analyze_query(query["query"])
        
        # Verify intent matches expected
        assert intent == query["expected_intent"]
        
        # Verify extracted entities
        for key, value in query["expected_entities"].items():
            assert key in entities
            assert value.lower() in entities[key].lower()

async def test_prolog_integration(hybrid_engine, test_queries):
    """Test Prolog integration within the hybrid engine."""
    for query in test_queries:
        # Get Prolog data
        prolog_data = hybrid_engine._get_prolog_data(
            query["expected_intent"],
            query["expected_entities"]
        )
        
        # Verify Prolog data structure
        assert isinstance(prolog_data, dict)
        
        # Verify data based on intent
        if query["expected_intent"] == "pest_identification":
            assert "pests" in prolog_data or "identified_pest" in prolog_data
        elif query["expected_intent"] == "control_methods":
            assert "control_methods" in prolog_data or "methods" in prolog_data
        elif query["expected_intent"] == "prevention":
            assert "prevention_methods" in prolog_data or "methods" in prolog_data

async def test_llm_enhancement(hybrid_engine, test_queries):
    """Test LLM enhancement of Prolog results."""
    for query in test_queries:
        # Get Prolog data first
        prolog_data = hybrid_engine._get_prolog_data(
            query["expected_intent"],
            query["expected_entities"]
        )
        
        # Get enhanced response
        enhanced_response = await hybrid_engine.llm.enhance_prolog_response(
            prolog_data,
            query["query"],
            crop_name=query["expected_entities"].get("crop")
        )
        
        # Verify enhanced response
        assert isinstance(enhanced_response, str)
        assert len(enhanced_response) > 0
        
        # Check if response includes key terms
        lower_response = enhanced_response.lower()
        for entity in query["expected_entities"].values():
            assert entity.lower() in lower_response

async def test_error_handling(client):
    """Test error handling in the chat API."""
    url = '/api/chat/'
    
    # Test empty message
    response = await client.post(
        url,
        data=json.dumps({"message": ""}),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Test invalid JSON
    response = await client.post(
        url,
        data="invalid json",
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Test missing message field
    response = await client.post(
        url,
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

async def test_response_consistency(client):
    """Test consistency of responses for the same query."""
    url = '/api/chat/'
    test_query = {
        "message": "How do I identify tomato hornworm?",
        "context": {}
    }
    
    # Make multiple requests with the same query
    responses = []
    for _ in range(3):
        response = await client.post(
            url,
            data=json.dumps(test_query),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        responses.append(response.json())
    
    # Verify confidence scores are consistent
    confidence_scores = [r['metadata']['confidence'] for r in responses]
    variance = max(confidence_scores) - min(confidence_scores)
    assert variance < 0.2  # Confidence scores shouldn't vary too much
