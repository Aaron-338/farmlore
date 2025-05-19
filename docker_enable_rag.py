#!/usr/bin/env python3
"""
Script to enable RAG in a Docker environment.
Assumes dependencies are already installed in the Docker container.
"""
import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def enable_rag_in_docker():
    """Enable RAG in the Docker environment."""
    # Set environment variable in the Docker container
    os.environ['USE_RAG'] = 'true'
    logger.info("Set USE_RAG environment variable to 'true'")
    
    # Set the persistent directory for ChromaDB
    os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
    logger.info("Set RAG_PERSIST_DIR to '/app/data/chromadb'")
    
    # Create the persistent directory if it doesn't exist
    persist_dir = os.environ['RAG_PERSIST_DIR']
    os.makedirs(persist_dir, exist_ok=True)
    logger.info(f"Created persistent directory at {persist_dir}")
    
    # Check if the application is running
    try:
        # Use docker-compose commands to check if the application is running
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=farmlore", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        running_containers = result.stdout.strip().split('\n')
        if running_containers and running_containers[0]:
            logger.info(f"Found running containers: {running_containers}")
            
            # Restart the web container to apply the environment variable
            logger.info("Restarting web container to apply RAG integration...")
            subprocess.run(["docker-compose", "restart", "web"])
            logger.info("Container restarted with RAG enabled")
        else:
            logger.info("No running containers found. Please start the application with:")
            logger.info("docker-compose up -d")
    except Exception as e:
        logger.error(f"Error interacting with Docker: {str(e)}")
        logger.info("To manually enable RAG:")
        logger.info("1. Add 'USE_RAG=true' and 'RAG_PERSIST_DIR=/app/data/chromadb' to your environment")
        logger.info("2. Restart your Docker containers: docker-compose restart web")
    
    print("\nRAG has been enabled in the Docker environment.")
    print("To verify it's working, check the logs with: docker-compose logs web")
    print("Look for messages about 'Successfully extended HybridEngine with RAG capabilities'")
    
    return True

def update_docker_compose():
    """Update docker-compose.yml file to include RAG environment variables."""
    try:
        docker_compose_file = "docker-compose.yml"
        
        # Check if the file exists
        if not os.path.exists(docker_compose_file):
            docker_compose_file = os.path.join("pest-management-chatbot", "docker-compose.yml")
            if not os.path.exists(docker_compose_file):
                logger.warning("docker-compose.yml file not found. Skipping update.")
                return False
        
        # Read the current content
        with open(docker_compose_file, 'r') as f:
            content = f.read()
        
        # Check if RAG environment variables are already present
        if "USE_RAG" in content:
            logger.info("RAG environment variables already present in docker-compose.yml")
            return True
        
        # Find the web service and its environment section
        web_service_index = content.find("  web:")
        if web_service_index == -1:
            logger.warning("Web service not found in docker-compose.yml. Skipping update.")
            return False
        
        # Find the environment section or create one
        env_section_index = content.find("    environment:", web_service_index)
        
        if env_section_index == -1:
            # No environment section, find a good place to add it
            lines = content.split('\n')
            web_service_line = -1
            for i, line in enumerate(lines):
                if line.strip() == "web:":
                    web_service_line = i
                    break
            
            if web_service_line == -1:
                logger.warning("Could not locate web service line. Skipping update.")
                return False
            
            # Add environment section after the web service
            for i in range(web_service_line + 1, len(lines)):
                if lines[i].startswith("  "):  # Find the first indented line
                    # Add environment section with the same indentation plus 2 spaces
                    indent = " " * (len(lines[i]) - len(lines[i].lstrip()) + 2)
                    lines.insert(i, f"{indent}environment:")
                    lines.insert(i + 1, f"{indent}  - USE_RAG=true")
                    lines.insert(i + 2, f"{indent}  - RAG_PERSIST_DIR=/app/data/chromadb")
                    break
            
            new_content = '\n'.join(lines)
        else:
            # Environment section exists, just add RAG variables
            env_end_index = content.find("\n", env_section_index)
            if env_end_index == -1:
                env_end_index = len(content)
            
            # Get the indentation level of the environment section
            env_line = content[env_section_index:env_end_index].strip()
            indent = " " * (len(content[env_section_index:env_end_index]) - len(env_line))
            
            # Add RAG variables with the same indentation
            rag_vars = f"\n{indent}  - USE_RAG=true\n{indent}  - RAG_PERSIST_DIR=/app/data/chromadb"
            new_content = content[:env_end_index] + rag_vars + content[env_end_index:]
        
        # Write the updated content
        with open(docker_compose_file, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully updated {docker_compose_file} with RAG environment variables")
        return True
    
    except Exception as e:
        logger.error(f"Error updating docker-compose.yml: {str(e)}")
        return False

if __name__ == "__main__":
    print("Enabling RAG in Docker environment...")
    
    # Update docker-compose.yml file
    print("\nUpdating docker-compose.yml...")
    if update_docker_compose():
        print("✓ docker-compose.yml updated with RAG environment variables")
    else:
        print("⚠ Could not update docker-compose.yml. You may need to add RAG environment variables manually.")
    
    # Enable RAG in running Docker containers
    print("\nEnabling RAG in running containers...")
    if enable_rag_in_docker():
        print("✓ RAG enabled in Docker environment")
    else:
        print("⚠ Could not enable RAG in Docker environment. See logs for details.") 