#!/usr/bin/env python
"""
Script to update docker-compose.yml for RAG integration.
"""
import os
import yaml
import shutil

def update_docker_compose():
    """Update docker-compose.yml to add RAG configuration."""
    # Read the current docker-compose.yml
    try:
        with open('docker-compose.yml', 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading docker-compose.yml: {e}")
        return False
    
    # Make a backup of the original file
    try:
        shutil.copy2('docker-compose.yml', 'docker-compose.yml.bak')
        print("Created backup of docker-compose.yml as docker-compose.yml.bak")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False
    
    # Update the volumes section to add chroma_data
    if 'volumes' in config:
        if 'chroma_data' not in config['volumes']:
            config['volumes']['chroma_data'] = {}
            print("Added chroma_data volume")
    else:
        print("Error: No volumes section found in docker-compose.yml")
        return False
    
    # Update the web service
    if 'services' in config and 'web' in config['services']:
        web_service = config['services']['web']
        
        # Update volumes for web service
        if 'volumes' in web_service:
            if 'chroma_data:/app/data/chromadb' not in web_service['volumes']:
                web_service['volumes'].append('chroma_data:/app/data/chromadb')
                print("Added chroma_data volume mount to web service")
        else:
            print("Error: No volumes section found in web service")
            return False
        
        # Update environment variables
        if 'environment' in web_service:
            # Add RAG environment variables if they don't exist
            rag_env_vars = {
                'USE_RAG': 'true',
                'RAG_PERSIST_DIR': '/app/data/chromadb'
            }
            
            # Convert environment from list to dict if necessary
            if isinstance(web_service['environment'], list):
                env_dict = {}
                for item in web_service['environment']:
                    if isinstance(item, str) and '=' in item:
                        key, value = item.split('=', 1)
                        env_dict[key.strip()] = value.strip()
                web_service['environment'] = env_dict
            
            # Add new environment variables
            for key, value in rag_env_vars.items():
                if key not in web_service['environment']:
                    web_service['environment'][key] = value
                    print(f"Added environment variable {key}={value}")
        else:
            print("Error: No environment section found in web service")
            return False
    else:
        print("Error: Web service not found in docker-compose.yml")
        return False
    
    # Save the updated configuration
    try:
        with open('docker-compose.yml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print("Updated docker-compose.yml successfully")
        return True
    except Exception as e:
        print(f"Error writing updated docker-compose.yml: {e}")
        return False

def check_rag_files():
    """Check if the necessary RAG files exist."""
    required_files = [
        'implement_rag.py',
        'hybrid_engine_patch.py',
        'requirements_rag.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Warning: The following RAG files are missing: {', '.join(missing_files)}")
        return False
    
    print("All required RAG files are present")
    return True

def create_target_directories():
    """Create target directories for RAG files if they don't exist."""
    target_dir = 'pest-management-chatbot/farmlore-project/api/inference_engine'
    
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir, exist_ok=True)
            print(f"Created directory: {target_dir}")
        except Exception as e:
            print(f"Error creating directory {target_dir}: {e}")
            return False
    
    return True

def copy_rag_files():
    """Copy RAG files to the appropriate target directories."""
    file_mappings = {
        'implement_rag.py': 'pest-management-chatbot/farmlore-project/api/inference_engine/implement_rag.py',
        'hybrid_engine_patch.py': 'pest-management-chatbot/farmlore-project/api/inference_engine/hybrid_engine_patch.py',
        'requirements_rag.txt': 'pest-management-chatbot/farmlore-project/requirements_rag.txt'
    }
    
    for source, target in file_mappings.items():
        if os.path.exists(source):
            try:
                target_dir = os.path.dirname(target)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                
                shutil.copy2(source, target)
                print(f"Copied {source} to {target}")
            except Exception as e:
                print(f"Error copying {source} to {target}: {e}")
        else:
            print(f"Warning: Source file {source} not found")
    
    return True

if __name__ == "__main__":
    print("Checking for RAG files...")
    check_rag_files()
    
    print("\nCreating target directories...")
    create_target_directories()
    
    print("\nCopying RAG files to target directories...")
    copy_rag_files()
    
    print("\nUpdating docker-compose.yml...")
    update_docker_compose()
    
    print("\nSetup complete! Next steps:")
    print("1. Review the changes to docker-compose.yml")
    print("2. Update the Dockerfile to install RAG dependencies")
    print("3. Add the RAG initialization code to start_web.sh")
    print("4. Update file paths in implement_rag.py if necessary")
    print("5. Rebuild and restart the Docker containers") 