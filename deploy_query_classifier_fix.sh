#!/bin/bash
# Deploy query classifier fix to Docker container

# Set variables
CONTAINER_NAME="farmlore-web-1"
PATCH_FILE="docker_fix_query_classifier.py"
CONTAINER_PATH="/app/"

echo "Deploying query classifier fix to Docker container..."

# Check if the container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
  echo "Error: Container $CONTAINER_NAME is not running."
  echo "Please make sure the container is running before deploying the fix."
  exit 1
fi

# Copy the patch file to the container
echo "Copying patch script to container..."
docker cp $PATCH_FILE $CONTAINER_NAME:$CONTAINER_PATH

# Execute the patch script in the container
echo "Executing the patch script in the container..."
docker exec $CONTAINER_NAME python /app/docker_fix_query_classifier.py

# Check if the script executed successfully
if [ $? -eq 0 ]; then
  echo "Patch applied successfully!"
  echo "The query classifier has been fixed."
  echo ""
  echo "You can now test with queries like:"
  echo "- 'What are natural predators for aphids?'"
  echo "- 'What beneficial insects eat aphids?'"
  echo "These will now be correctly classified as pest management queries."
else
  echo "Error: Failed to apply the patch."
  echo "Check the container logs for more details."
  exit 1
fi

# Optional: Display web service logs
echo ""
echo "Displaying web service logs to confirm patch (press Ctrl+C to stop)..."
docker logs -f $CONTAINER_NAME 