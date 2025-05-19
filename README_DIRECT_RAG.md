# Direct RAG Integration for Docker

This approach provides a more reliable method for integrating RAG (Retrieval-Augmented Generation) capabilities with the HybridEngine in a Docker environment. Instead of using method patching, which can be fragile, this approach uses class inheritance and module replacement to ensure a more robust integration.

## How It Works

The direct approach works by:

1. Creating a new class (`EnhancedHybridEngine`) that inherits from the original `HybridEngine`
2. Overriding the `query` method to add RAG capabilities
3. Replacing the original `HybridEngine` class in the module at runtime

This approach avoids the pitfalls of method patching, which can be unreliable in complex environments like Docker containers.

## Files Included

- `docker_query_wrapper.py`: The main module that implements the direct RAG integration
- `install_rag_docker_wrapper.sh`: Shell script to deploy the RAG integration to a running Docker container
- `install_rag_wrapper.bat`: Windows batch script to run the installation
- `test_rag_wrapper.py`: Script to test and verify the RAG integration

## Installation Instructions

### Using Windows

1. Make sure your Docker container is running
2. Run `install_rag_wrapper.bat`

### Using Linux/Mac

1. Make sure your Docker container is running
2. Run `bash install_rag_docker_wrapper.sh`

### Manual Installation

If the scripts don't work for your environment, you can perform these steps manually:

1. Copy `docker_query_wrapper.py` to `/app/api/inference_engine/` in your Docker container
2. Create and copy `start_web_rag.sh` to `/app/` in your Docker container
3. Make `start_web_rag.sh` executable
4. Install required packages in the container: `langchain-community huggingface_hub sentence-transformers chromadb`
5. Restart the web service using the new script

## Verifying Installation

After installation, you can verify that RAG is working correctly by:

1. Running `test_rag_wrapper.py` inside the Docker container
2. Making API requests to test RAG-enhanced responses
3. Checking the logs for RAG-related messages

## Troubleshooting

If you encounter issues:

1. Check Docker container logs for errors
2. Verify all required packages are installed
3. Make sure the vector store directory exists at `/app/data/chromadb`
4. Ensure the RAG system is properly initialized before queries are made

## Advantages Over Method Patching

This direct approach offers several advantages:

- **Reliability**: Class inheritance is more stable than method patching
- **Simplicity**: The implementation is easier to understand and maintain
- **Resilience**: Works even if the original code structure changes slightly
- **Transparency**: Changes are more visible in the code

## How to Extend

This implementation can be extended by:

1. Adding more RAG capabilities to the `RAGQueryIntegration` class
2. Implementing additional data sources for the vector store
3. Fine-tuning the RAG query process for better results
4. Adding metrics and monitoring for RAG performance 