#!/usr/bin/env python
"""
Simple script to integrate RAG capabilities directly into HybridEngine.
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_rag_to_hybrid_engine():
    """
    Add RAG capabilities directly to HybridEngine.
    """
    try:
        # Try to import the necessary modules
        from api.inference_engine.hybrid_engine import HybridEngine
        from api.inference_engine.implement_rag import extend_hybrid_engine
        
        # Get the HybridEngine instance
        # Either import it from where it's created as a singleton,
        # or create a new instance if necessary
        try:
            logger.info("Attempting to import hybrid_engine instance...")
            from api.inference_engine import hybrid_engine
            engine = hybrid_engine
            logger.info("Successfully imported existing hybrid_engine instance")
            
            # Print available methods to help debug
            method_list = [m for m in dir(engine) if not m.startswith('_') and callable(getattr(engine, m))]
            logger.info(f"Available methods in HybridEngine: {method_list}")
            
        except (ImportError, AttributeError) as e:
            logger.info(f"Could not import existing hybrid_engine instance: {str(e)}")
            logger.info("Creating new HybridEngine instance...")
            engine = HybridEngine()
            logger.info("Created new HybridEngine instance")
            
            # Print available methods to help debug
            method_list = [m for m in dir(engine) if not m.startswith('_') and callable(getattr(engine, m))]
            logger.info(f"Available methods in HybridEngine: {method_list}")
        
        # Print if engine is already extended with RAG
        if hasattr(engine, 'rag_system'):
            logger.info("HybridEngine already has rag_system attribute")
        
        print("Found existing HybridEngine instance, extending with RAG")
        # Extend the HybridEngine with RAG capabilities
        extend_hybrid_engine(engine)
        logger.info("Successfully extended HybridEngine with RAG capabilities")
        
        return True
    except Exception as e:
        logger.error(f"Error adding RAG to HybridEngine: {str(e)}")
        print(f"Error integrating RAG with HybridEngine: {str(e)}")
        return False

def update_docker_compose_yml():
    """
    Update docker-compose.yml to add RAG-related volumes and environment variables.
    """
    try:
        import yaml
        
        # Check if docker-compose.yml exists
        if not os.path.exists('docker-compose.yml'):
            logger.error("docker-compose.yml not found")
            return False
        
        # Make a backup
        if not os.path.exists('docker-compose.yml.bak'):
            import shutil
            shutil.copy2('docker-compose.yml', 'docker-compose.yml.bak')
            logger.info("Created backup of docker-compose.yml as docker-compose.yml.bak")
        
        # Read docker-compose.yml
        with open('docker-compose.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Add volume if not exists
        if 'volumes' in config and 'chroma_data' not in config['volumes']:
            config['volumes']['chroma_data'] = None
            logger.info("Added chroma_data volume")
        
        # Update web service
        if 'services' in config and 'web' in config['services']:
            web = config['services']['web']
            
            # Add volume to web service
            if 'volumes' in web:
                volume_mount = 'chroma_data:/app/data/chromadb'
                if volume_mount not in web['volumes']:
                    web['volumes'].append(volume_mount)
                    logger.info(f"Added {volume_mount} to web service volumes")
            
            # Add environment variables to web service
            if 'environment' in web:
                env_vars = {
                    'USE_RAG': 'true',
                    'RAG_PERSIST_DIR': '/app/data/chromadb'
                }
                
                # Handle both list and dict formats for environment
                if isinstance(web['environment'], list):
                    # List format
                    for key, value in env_vars.items():
                        env_var = f"{key}={value}"
                        if env_var not in web['environment']:
                            web['environment'].append(env_var)
                            logger.info(f"Added {env_var} to web service environment")
                else:
                    # Dict format
                    for key, value in env_vars.items():
                        if key not in web['environment']:
                            web['environment'][key] = value
                            logger.info(f"Added {key}={value} to web service environment")
        
        # Write updated docker-compose.yml
        with open('docker-compose.yml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
        logger.info("Successfully updated docker-compose.yml")
        return True
    except Exception as e:
        logger.error(f"Error updating docker-compose.yml: {str(e)}")
        return False

def update_requirements():
    """
    Update requirements.txt to include RAG dependencies.
    """
    rag_requirements = """
# RAG requirements
langchain==0.1.8
langchain-community==0.0.19
chromadb==0.4.24
sentence-transformers==2.5.1
huggingface-hub==0.20.3
pysbd==0.3.4
regex==2023.12.25
"""
    
    # Check if requirements.txt exists
    req_file_path = 'requirements.txt'
    if not os.path.exists(req_file_path):
        req_file_path = 'pest-management-chatbot/farmlore-project/requirements.txt'
        if not os.path.exists(req_file_path):
            logger.error("requirements.txt not found")
            return False
    
    try:
        # Make a backup
        import shutil
        backup_path = f"{req_file_path}.bak"
        if not os.path.exists(backup_path):
            shutil.copy2(req_file_path, backup_path)
            logger.info(f"Created backup of {req_file_path} as {backup_path}")
        
        # Read requirements.txt
        with open(req_file_path, 'r') as f:
            content = f.read()
        
        # Check if RAG requirements are already added
        if 'langchain' in content and 'chromadb' in content:
            logger.info("RAG requirements already present in requirements.txt")
            return True
        
        # Add RAG requirements
        with open(req_file_path, 'a') as f:
            f.write(rag_requirements)
        
        logger.info(f"Successfully updated {req_file_path} with RAG requirements")
        return True
    except Exception as e:
        logger.error(f"Error updating requirements.txt: {str(e)}")
        return False

if __name__ == "__main__":
    print("==== Integrating RAG with FarmLore System ====")
    
    print("\n1. Updating docker-compose.yml...")
    update_docker_compose_yml()
    
    print("\n2. Updating requirements...")
    update_requirements()
    
    print("\n3. Adding RAG to HybridEngine...")
    add_rag_to_hybrid_engine()
    
    print("\nIntegration complete!")
    print("\nNext steps:")
    print("1. Rebuild the Docker image: docker-compose build web")
    print("2. Restart the containers: docker-compose up -d")
    print("3. Check logs: docker-compose logs -f web") 