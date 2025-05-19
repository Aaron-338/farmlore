#!/usr/bin/env python
"""
Script to update Dockerfile to include RAG dependencies.
"""
import os
import re
import shutil

def update_dockerfile(dockerfile_path='Dockerfile'):
    """Update Dockerfile to install RAG dependencies."""
    # Check if Dockerfile exists
    if not os.path.exists(dockerfile_path):
        print(f"Error: {dockerfile_path} not found")
        return False
    
    # Make a backup of the original file
    try:
        backup_path = f"{dockerfile_path}.bak"
        shutil.copy2(dockerfile_path, backup_path)
        print(f"Created backup of {dockerfile_path} as {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False
    
    # Read the current Dockerfile
    try:
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
    except Exception as e:
        print(f"Error reading {dockerfile_path}: {e}")
        return False
    
    # Check if RAG requirements are already added
    if "requirements_rag.txt" in dockerfile_content:
        print("RAG requirements already added to Dockerfile.")
        return True
    
    # Find the position to insert the RAG requirements
    main_requirements_pattern = r"(COPY .*requirements\.txt .*\nRUN pip install --no-cache-dir -r requirements\.txt)"
    match = re.search(main_requirements_pattern, dockerfile_content)
    
    if not match:
        print("Error: Could not find the requirements.txt installation section in the Dockerfile")
        return False
    
    # Prepare the RAG requirements section
    rag_requirements_section = "\n\n# Install RAG requirements\nCOPY pest-management-chatbot/farmlore-project/requirements_rag.txt .\nRUN pip install --no-cache-dir -r requirements_rag.txt"
    
    # Insert the RAG requirements after the main requirements
    new_content = dockerfile_content[:match.end()] + rag_requirements_section + dockerfile_content[match.end():]
    
    # Write the updated Dockerfile
    try:
        with open(dockerfile_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {dockerfile_path} with RAG requirements")
        return True
    except Exception as e:
        print(f"Error writing updated {dockerfile_path}: {e}")
        return False

def update_start_web_script(script_path='pest-management-chatbot/farmlore-project/start_web.sh'):
    """Update start_web.sh to initialize RAG system."""
    # Check if script exists
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found")
        return False
    
    # Make a backup of the original file
    try:
        backup_path = f"{script_path}.bak"
        shutil.copy2(script_path, backup_path)
        print(f"Created backup of {script_path} as {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False
    
    # Read the current script
    try:
        with open(script_path, 'r') as f:
            script_content = f.read()
    except Exception as e:
        print(f"Error reading {script_path}: {e}")
        return False
    
    # Check if RAG initialization is already added
    if "Initialize RAG" in script_content:
        print("RAG initialization already added to start_web.sh")
        return True
    
    # Prepare the RAG initialization code
    rag_init_code = """
# Initialize RAG if enabled
if [ "$USE_RAG" = "true" ]; then
    echo "Initializing RAG system..."
    python -c "
import logging
logging.basicConfig(level=logging.INFO)
try:
    from api.inference_engine.implement_rag import PrologToRAGConverter
    converter = PrologToRAGConverter(persist_directory='${RAG_PERSIST_DIR}')
    vector_store = converter.process_all_knowledge_bases()
    if vector_store:
        logging.info('RAG vector store successfully created/loaded')
    else:
        logging.error('Failed to initialize RAG vector store')
except Exception as e:
    logging.error(f'Error initializing RAG: {str(e)}')
"
fi
"""
    
    # Find where to insert the RAG initialization code
    # Usually, we want to add it before the web server starts
    start_server_pattern = r"(python manage\.py runserver|gunicorn)"
    match = re.search(start_server_pattern, script_content)
    
    if match:
        # Insert RAG initialization before the server starts
        insert_pos = script_content.rfind('\n', 0, match.start())
        if insert_pos == -1:
            insert_pos = 0
        
        new_content = script_content[:insert_pos] + rag_init_code + script_content[insert_pos:]
    else:
        # If we can't find the server start command, append to the end of the file
        new_content = script_content.rstrip() + "\n" + rag_init_code
    
    # Write the updated script
    try:
        with open(script_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {script_path} with RAG initialization code")
        return True
    except Exception as e:
        print(f"Error writing updated {script_path}: {e}")
        return False

def update_hybrid_engine_init(init_path='pest-management-chatbot/farmlore-project/api/inference_engine/__init__.py'):
    """Update __init__.py to apply RAG patches to HybridEngine."""
    # Create directory if it doesn't exist
    init_dir = os.path.dirname(init_path)
    if not os.path.exists(init_dir):
        try:
            os.makedirs(init_dir, exist_ok=True)
            print(f"Created directory: {init_dir}")
        except Exception as e:
            print(f"Error creating directory {init_dir}: {e}")
            return False
    
    # Check if file exists and make backup if needed
    if os.path.exists(init_path):
        try:
            backup_path = f"{init_path}.bak"
            shutil.copy2(init_path, backup_path)
            print(f"Created backup of {init_path} as {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    # Read existing content or create new file
    try:
        if os.path.exists(init_path):
            with open(init_path, 'r') as f:
                init_content = f.read()
        else:
            init_content = "# Inference engine initialization\n"
    except Exception as e:
        print(f"Error reading {init_path}: {e}")
        return False
    
    # Check if RAG initialization is already added
    if "Apply RAG patches" in init_content:
        print("RAG patches already added to __init__.py")
        return True
    
    # Prepare RAG initialization code
    rag_init_code = """
# Initialize the HybridEngine with RAG if enabled
import os
from api.inference_engine.hybrid_engine import HybridEngine

# Create singleton instance
hybrid_engine = HybridEngine()

# Apply RAG patches if enabled
if os.environ.get('USE_RAG', 'false').lower() == 'true':
    try:
        from api.inference_engine.hybrid_engine_patch import HybridEnginePatch
        HybridEnginePatch.apply_patches(hybrid_engine)
    except Exception as e:
        import logging
        logging.error(f"Failed to apply RAG patches: {str(e)}")
"""
    
    # Append RAG code to the end of the file
    new_content = init_content.rstrip() + "\n\n" + rag_init_code
    
    # Write the updated init file
    try:
        with open(init_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {init_path} with RAG initialization code")
        return True
    except Exception as e:
        print(f"Error writing updated {init_path}: {e}")
        return False

def update_implement_rag_paths(rag_impl_path='pest-management-chatbot/farmlore-project/api/inference_engine/implement_rag.py'):
    """Update file paths in implement_rag.py to use absolute Docker paths."""
    if not os.path.exists(rag_impl_path):
        print(f"Error: {rag_impl_path} not found")
        return False
    
    try:
        with open(rag_impl_path, 'r') as f:
            rag_content = f.read()
    except Exception as e:
        print(f"Error reading {rag_impl_path}: {e}")
        return False
    
    # Make a backup of the original file
    try:
        backup_path = f"{rag_impl_path}.bak"
        shutil.copy2(rag_impl_path, backup_path)
        print(f"Created backup of {rag_impl_path} as {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
    
    # Update file paths pattern
    file_paths_pattern = r"prolog_files\s*=\s*\[(.*?)\]"
    match = re.search(file_paths_pattern, rag_content, re.DOTALL)
    
    if not match:
        print(f"Error: Could not find prolog_files list in {rag_impl_path}")
        return False
    
    # Create the new file paths list
    new_file_paths = """prolog_files = [
        '/app/knowledgebase_docker.pl',
        '/app/pea_updates_docker.pl',
        '/app/advanced_queries_docker.pl'
    ]"""
    
    # Replace the old file paths list with the new one
    new_content = rag_content[:match.start()] + new_file_paths + rag_content[match.end():]
    
    # Write the updated file
    try:
        with open(rag_impl_path, 'w') as f:
            f.write(new_content)
        print(f"Updated file paths in {rag_impl_path}")
        return True
    except Exception as e:
        print(f"Error writing updated {rag_impl_path}: {e}")
        return False

if __name__ == "__main__":
    print("Updating Dockerfile to install RAG dependencies...")
    update_dockerfile()
    
    print("\nUpdating start_web.sh to initialize RAG system...")
    update_start_web_script()
    
    print("\nSetting up HybridEngine initialization with RAG...")
    update_hybrid_engine_init()
    
    print("\nUpdating file paths in implement_rag.py...")
    update_implement_rag_paths()
    
    print("\nSetup complete! Next steps:")
    print("1. Ensure all updated files are correctly placed in the Docker build context")
    print("2. Rebuild the Docker image with 'docker-compose build web'")
    print("3. Restart the containers with 'docker-compose up -d'")
    print("4. Check the logs with 'docker-compose logs -f web' to verify RAG initialization") 