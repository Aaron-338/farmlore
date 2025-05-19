# Embeddings-Based Query Classifier

This directory contains an alternative implementation of the query classification system using vector embeddings and semantic similarity instead of hardcoded keywords.

## Overview

The embeddings classifier uses a pre-trained sentence transformer model to convert queries into high-dimensional vectors and classify them by measuring similarity to example queries for each category.

### Benefits Over Keyword-Based Approach

- More robust to different phrasings of the same question
- No need to manually update keyword lists
- Better handles complex semantic relationships
- Improved performance on edge cases
- More maintainable over time

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed
- Alternatively, Python 3.8+ with pip

### Running with Docker (Recommended)

#### Run the embeddings classifier test:

```bash
# On Windows
run_embeddings_docker.bat

# On Linux/macOS
chmod +x run_embeddings_docker.sh
./run_embeddings_docker.sh
```

#### Run the embeddings classifier API:

```bash
# On Windows
run_embeddings_api.bat

# On Linux/macOS
chmod +x run_embeddings_api.sh
./run_embeddings_api.sh
```

#### Test the API:

```bash
python test_api.py
```

### Running without Docker (Local Development)

```bash
# Install dependencies
pip install -r requirements-embeddings.txt

# Run the classifier
python embeddings_classifier.py

# Run the API
python embeddings_classifier_api.py

# Run the comparison test
python test_compare_classifiers.py
```

## API Endpoints

The embeddings classifier provides a simple REST API:

### Health Check

```
GET /health
```

Returns the API service status.

### Classify Query

```
POST /classify
```

Request body:
```json
{
  "query": "My tomato leaves have yellow spots"
}
```

Response:
```json
{
  "success": true,
  "query": "My tomato leaves have yellow spots",
  "classification": "pest_identification"
}
```

## Integration with Existing System

To integrate this classifier with your existing RAG system:

1. Add the embeddings classifier to your imports:
```python
from embeddings_classifier import detect_prompt_type_embeddings
```

2. Replace the existing classifier in api/views.py (chat_api function):
```python
# Change this line:
prompt_type = detect_prompt_type(message)

# To use the embeddings classifier instead:
prompt_type = detect_prompt_type_embeddings(message)
```

Alternatively, you can use the API service in a microservices architecture.

## Comparing Classifiers

To compare the embeddings classifier with the keyword-based approach:

```bash
# Using Docker
docker-compose -f docker-compose.embeddings.yml up compare-classifiers

# Without Docker
python test_compare_classifiers.py
```

This will run both classifiers on a set of test queries and show where they agree or disagree.

## Customization

You can customize the embeddings classifier by:

1. Adding more example queries to each category in `embeddings_classifier.py`
2. Using a different pre-trained model by changing the `model_name` parameter
3. Adjusting the similarity threshold (currently 0.5) 