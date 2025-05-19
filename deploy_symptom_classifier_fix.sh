#!/bin/bash
# Deploy symptom classification fix to the farmlore system

# Set up error handling
set -e

echo "====================================================="
echo "  Deploying Symptom Query Classification Fix"
echo "====================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker does not seem to be running. Please start Docker first."
    exit 1
fi

# Check for the improved patch file
if [ ! -f "improved_patch_classifier.py" ]; then
    echo "Error: improved_patch_classifier.py not found in the current directory."
    exit 1
fi

# Check for the test file
if [ ! -f "test_symptom_classification.py" ]; then
    echo "Error: test_symptom_classification.py not found in the current directory."
    exit 1
fi

# Determine container name
CONTAINER_NAME=$(docker ps --format '{{.Names}}' | grep farmlore | head -n 1)
if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: No farmlore containers found running."
    exit 1
fi

echo "Found farmlore container: $CONTAINER_NAME"

# Copy the improved patch file to the container
echo "Copying improved_patch_classifier.py to container..."
docker cp improved_patch_classifier.py $CONTAINER_NAME:/app/

# Copy the test file to the container
echo "Copying test_symptom_classification.py to container..."
docker cp test_symptom_classification.py $CONTAINER_NAME:/app/

# Run the patch in the container
echo "Applying the symptom classification patch..."
docker exec $CONTAINER_NAME python /app/improved_patch_classifier.py

# Verify the fix with the test script
echo "Testing the symptom classification patch..."
docker exec $CONTAINER_NAME python /app/test_symptom_classification.py

echo
echo "====================================================="
echo "  Symptom Classification Fix Deployed Successfully"
echo "====================================================="
echo
echo "The system should now correctly classify symptom-based queries!"
echo "Example queries that will now work:"
echo "  - 'My crops are turning purple'"
echo "  - 'Why are my tomato leaves yellow?'"
echo "  - 'My plants are wilting despite watering'"
echo "  - 'What's wrong with my plant with holes in the leaves?'"
echo
echo "These queries will be routed to the PEST_IDENTIFICATION handler,"
echo "which can access both pest and disease information to provide"
echo "appropriate responses."
echo "=====================================================" 