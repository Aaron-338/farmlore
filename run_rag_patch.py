#!/usr/bin/env python
"""
Script to run when the container starts to apply the RAG patch
"""
import os
import sys
import logging
import time
import signal
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("rag_patch_runner")

def copy_files_to_container():
    """Copy the necessary files to the container"""
    try:
        # First check which container we're in
        container_id = subprocess.check_output("hostname", shell=True).decode().strip()
        logger.info(f"Running in container: {container_id}")
        
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Current directory: {current_dir}")
        
        # Create the necessary directories
        os.makedirs("/app/data/chromadb", exist_ok=True)
        
        # Set environment variables
        os.environ["USE_RAG"] = "true"
        os.environ["RAG_PERSIST_DIR"] = "/app/data/chromadb"
        
        logger.info("Environment variables set")
        return True
    except Exception as e:
        logger.error(f"Error copying files: {str(e)}")
        return False

def initialize_rag():
    """Initialize the RAG system"""
    try:
        logger.info("Initializing RAG system...")
        # Import the initialization module
        sys.path.append('/app')
        
        from initialize_rag import initialize_rag as init_rag
        
        # Run initialization
        success = init_rag()
        logger.info(f"RAG initialization: {'SUCCESS' if success else 'FAILED'}")
        
        return success
    except Exception as e:
        logger.error(f"Error initializing RAG: {str(e)}")
        return False

def apply_rag_patch():
    """Apply the RAG patch to the HybridEngine"""
    try:
        logger.info("Applying RAG patch...")
        
        # Import the patch module
        from docker_direct_patch import apply_direct_patch
        
        # Run the patch
        success = apply_direct_patch()
        logger.info(f"RAG patch application: {'SUCCESS' if success else 'FAILED'}")
        
        return success
    except Exception as e:
        logger.error(f"Error applying RAG patch: {str(e)}")
        return False

def main():
    """Main function"""
    try:
        logger.info("Starting RAG patch runner...")
        
        # Wait for the container to fully initialize
        logger.info("Waiting for container to initialize (10 seconds)...")
        time.sleep(10)
        
        # Copy files
        if not copy_files_to_container():
            logger.error("Failed to copy files to container")
            return False
        
        # Initialize RAG
        if not initialize_rag():
            logger.error("Failed to initialize RAG")
            return False
        
        # Apply RAG patch
        if not apply_rag_patch():
            logger.error("Failed to apply RAG patch")
            return False
        
        logger.info("RAG patch successfully applied!")
        return True
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("Successfully applied RAG patch to HybridEngine")
        sys.exit(0)
    else:
        logger.error("Failed to apply RAG patch to HybridEngine")
        sys.exit(1) 