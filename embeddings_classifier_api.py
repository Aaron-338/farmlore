#!/usr/bin/env python
"""
API for Embeddings-based Query Classifier

Provides a REST API to the embeddings-based classifier.
"""

import logging
from flask import Flask, request, jsonify
from embeddings_classifier import EmbeddingsClassifier, PromptType

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Initialize classifier - will be lazy-loaded
classifier = None

def get_classifier():
    """Get or initialize the classifier instance"""
    global classifier
    if classifier is None:
        logger.info("Initializing embeddings classifier...")
        classifier = EmbeddingsClassifier()
        logger.info("Embeddings classifier initialized successfully")
    return classifier

@app.route('/classify', methods=['POST'])
def classify_query():
    """
    Classify a query using embeddings
    
    Request format:
    {
        "query": "string"
    }
    """
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'No query provided'
            }), 400
            
        query = data.get('query')
        logger.info(f"Received classification request for query: '{query}'")
        
        # Get classifier and classify the query
        cls = get_classifier()
        result = cls.classify(query)
        
        # Format the result
        if isinstance(result, PromptType):
            classification = result.value
        else:
            classification = str(result)
        
        logger.info(f"Classified '{query}' as {classification}")
        
        return jsonify({
            'success': True,
            'query': query,
            'classification': classification
        })
        
    except Exception as e:
        logger.error(f"Error in API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'embeddings-classifier-api'
    })

if __name__ == "__main__":
    logger.info("Starting embeddings classifier API...")
    app.run(host='0.0.0.0', port=5000, debug=True) 