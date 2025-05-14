"""
Test script to simulate real-world usage of specialized models and collect performance metrics.
This script:
1. Simulates queries of different types
2. Records performance metrics
3. Generates a performance report
"""
import os
import sys
import time
import json
import random
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

# Import necessary modules
try:
    from api.monitoring.model_performance import (
        record_model_response,
        record_model_feedback,
        get_model_performance_stats,
        get_query_type_stats,
        save_current_metrics
    )
    monitoring_available = True
except ImportError:
    logger.warning("Monitoring module not available. Performance metrics will not be recorded.")
    monitoring_available = False

# Sample test queries for each query type
TEST_QUERIES = {
    "pest_identification": [
        "I found small green insects on my tomato plants. What are they?",
        "There are white powdery spots on my cucumber leaves. What pest is this?",
        "My corn has small holes in the leaves. What could be causing this?",
        "I see small black beetles on my potato plants. Can you identify them?",
        "There are tiny white flies around my plants. What are they?"
    ],
    "pest_management": [
        "How do I control aphids on my tomatoes?",
        "What's the best organic method to control cucumber beetles?",
        "How can I prevent whiteflies in my garden?",
        "What's an effective treatment for spider mites?",
        "How do I get rid of cabbage worms naturally?"
    ],
    "crop_pests": [
        "What pests commonly affect tomato plants?",
        "What are the major pests of rice crops?",
        "Which insects typically attack corn plants?",
        "What pests should I watch for on my cabbage plants?",
        "What are common bean plant pests?"
    ],
    "indigenous_knowledge": [
        "What traditional methods are used to control pests in maize farming?",
        "How do indigenous farmers in Africa protect crops from insects?",
        "What natural pest control methods were used by Native Americans?",
        "Tell me about traditional pest management techniques in India",
        "What ash-based methods are used in traditional farming?"
    ],
    "general_query": [
        "How often should I water tomato plants?",
        "What's the best soil for growing vegetables?",
        "When is the best time to plant corn?",
        "How do I improve soil fertility naturally?",
        "What are good companion plants for beans?"
    ]
}

# Mapping of query types to specialized models
MODEL_MAPPING = {
    "pest_identification": "farmlore-pest-id",
    "pest_management": "farmlore-pest-mgmt",
    "crop_pests": "farmlore-crop-pests",
    "indigenous_knowledge": "farmlore-indigenous",
    "general_query": "farmlore-general"
}

# For control_methods, use the pest_management model
MODEL_MAPPING["control_methods"] = MODEL_MAPPING["pest_management"]

def simulate_model_response(query: str, query_type: str) -> Dict[str, Any]:
    """
    Simulate a model response for a given query.
    
    Args:
        query: The query text
        query_type: The type of query
    
    Returns:
        Dictionary with response details
    """
    # Get the appropriate model for this query type
    model_name = MODEL_MAPPING.get(query_type, "default-model")
    
    # Simulate processing time (faster for specialized models)
    base_time = 0.5  # Base response time in seconds
    specialized_factor = 0.7  # Specialized models are faster
    response_time = base_time * (specialized_factor if model_name.startswith("farmlore-") else 1.0)
    response_time *= (1 + random.uniform(-0.2, 0.2))  # Add some randomness
    
    # Simulate token usage
    tokens_in = len(query.split()) + random.randint(5, 15)  # Approximate input tokens
    tokens_out = random.randint(50, 200)  # Output tokens
    
    # Simulate success rate (higher for specialized models)
    success_probability = 0.95 if model_name.startswith("farmlore-") else 0.85
    success = random.random() < success_probability
    
    # Simulate processing
    time.sleep(0.1)  # Small delay to simulate actual processing
    
    # Record the response if monitoring is available
    if monitoring_available:
        record_model_response(
            model_name=model_name,
            query_type=query_type,
            response_time=response_time,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            success=success
        )
    
    return {
        "model_name": model_name,
        "query_type": query_type,
        "response_time": response_time,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "success": success
    }

def simulate_user_feedback(model_name: str) -> str:
    """
    Simulate user feedback for a model response.
    
    Args:
        model_name: The name of the model
    
    Returns:
        Feedback type (positive, negative, neutral)
    """
    # Specialized models get better feedback
    if model_name.startswith("farmlore-"):
        weights = [0.8, 0.1, 0.1]  # positive, negative, neutral
    else:
        weights = [0.6, 0.2, 0.2]  # positive, negative, neutral
    
    feedback = random.choices(["positive", "negative", "neutral"], weights=weights)[0]
    
    # Record the feedback if monitoring is available
    if monitoring_available:
        record_model_feedback(model_name, feedback)
    
    return feedback

def run_simulation(num_queries: int = 100, distribution: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Run a simulation with a specified number of queries.
    
    Args:
        num_queries: Number of queries to simulate
        distribution: Distribution of query types (if None, uses equal distribution)
    
    Returns:
        Dictionary with simulation results
    """
    logger.info(f"Starting simulation with {num_queries} queries")
    
    # Set default distribution if none provided
    if distribution is None:
        query_types = list(TEST_QUERIES.keys())
        distribution = {qt: 1.0 / len(query_types) for qt in query_types}
    
    # Validate distribution
    total = sum(distribution.values())
    if abs(total - 1.0) > 0.01:
        logger.warning(f"Distribution values sum to {total}, not 1.0. Normalizing.")
        distribution = {k: v / total for k, v in distribution.items()}
    
    # Calculate query counts for each type
    query_counts = {}
    remaining = num_queries
    for qt, prob in distribution.items():
        if qt == list(distribution.keys())[-1]:
            # Last item gets the remainder to ensure we hit exactly num_queries
            query_counts[qt] = remaining
        else:
            count = int(num_queries * prob)
            query_counts[qt] = count
            remaining -= count
    
    # Run the simulation
    results = {
        "total_queries": num_queries,
        "query_distribution": query_counts,
        "start_time": datetime.now().isoformat(),
        "responses": [],
        "feedback": {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }
    }
    
    for query_type, count in query_counts.items():
        logger.info(f"Processing {count} queries of type '{query_type}'")
        
        for _ in range(count):
            # Select a random query of this type
            query = random.choice(TEST_QUERIES[query_type])
            
            # Simulate the response
            response = simulate_model_response(query, query_type)
            results["responses"].append(response)
            
            # Simulate user feedback
            feedback = simulate_user_feedback(response["model_name"])
            results["feedback"][feedback] += 1
            
            # Small delay between queries
            time.sleep(0.05)
    
    results["end_time"] = datetime.now().isoformat()
    
    # Save the current metrics
    if monitoring_available:
        save_current_metrics()
    
    return results

def generate_performance_report() -> Dict[str, Any]:
    """
    Generate a performance report based on collected metrics.
    
    Returns:
        Dictionary with performance report
    """
    if not monitoring_available:
        return {"error": "Monitoring module not available"}
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "model_stats": get_model_performance_stats(),
        "query_type_stats": get_query_type_stats()
    }
    
    return report

def save_report(report: Dict[str, Any], filename: str = None):
    """
    Save a report to a JSON file.
    
    Args:
        report: The report to save
        filename: The filename to save to (if None, generates a default name)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_report_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Saved report to {filename}")
    except Exception as e:
        logger.error(f"Failed to save report: {str(e)}")

def main():
    """Main function to run the simulation and generate a report."""
    logger.info("Starting model performance test")
    
    # Define a realistic query distribution
    distribution = {
        "pest_identification": 0.25,
        "pest_management": 0.20,
        "crop_pests": 0.15,
        "indigenous_knowledge": 0.10,
        "general_query": 0.30
    }
    
    # Run the simulation
    results = run_simulation(num_queries=200, distribution=distribution)
    
    # Generate a performance report
    report = generate_performance_report()
    
    # Combine results and report
    combined = {
        "simulation_results": results,
        "performance_report": report
    }
    
    # Save the combined report
    save_report(combined, "model_performance_test_results.json")
    
    logger.info("Model performance test completed")

if __name__ == "__main__":
    main()
