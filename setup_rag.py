#!/usr/bin/env python
"""
Complete setup script for RAG integration with FarmLore.
This script sets up everything needed for RAG to work with the existing system.
"""
import os
import sys
import shutil
import logging
import re
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("rag_setup")

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DOCKER_COMPOSE_PATH = os.path.join(PROJECT_ROOT, "docker-compose.yml")
DOCKERFILE_PATH = os.path.join(PROJECT_ROOT, "Dockerfile")
APP_DIR = os.path.join(PROJECT_ROOT, "pest-management-chatbot", "farmlore-project")
START_WEB_SCRIPT = os.path.join(APP_DIR, "start_web.sh")
API_DIR = os.path.join(PROJECT_ROOT, "api")
INFERENCE_ENGINE_DIR = os.path.join(API_DIR, "inference_engine")

# Source files to create
source_files = {
    "implement_rag.py": os.path.join(INFERENCE_ENGINE_DIR, "implement_rag.py"),
    "initialize_rag.py": os.path.join(APP_DIR, "initialize_rag.py"),
}

def create_implement_rag():
    """Create the implement_rag.py file."""
    content = '''import os
import logging
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PrologToRAGConverter:
    """
    Convert Prolog frames into text chunks for RAG system and
    store them in a vector database.
    """
    
    def __init__(self, embedding_model="all-MiniLM-L6-v2", persist_directory=None):
        """
        Initialize the converter with the embedding model and storage location
        
        Args:
            embedding_model: HuggingFace model name for embeddings
            persist_directory: Directory to persist the vector database
        """
        self.embed_model = embedding_model
        
        # Use environment variable if available, otherwise use default
        if persist_directory is None:
            self.persist_directory = os.environ.get('RAG_PERSIST_DIR', './data/chromadb')
        else:
            self.persist_directory = persist_directory
            
        logger.info(f"Using persistence directory: {self.persist_directory}")
        
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Create the persist directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
    
    def _parse_prolog_file(self, file_path):
        """
        Parse a Prolog file and extract frames
        
        Args:
            file_path: Path to the Prolog file
            
        Returns:
            List of text chunks representing frames
        """
        logger.info(f"Parsing Prolog file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frame definitions with regex
            frame_pattern = r"frame\((\w+),\s*\[(.*?)\]\)"
            frames_raw = re.findall(frame_pattern, content, re.DOTALL)
            
            text_chunks = []
            for frame_type, frame_content in frames_raw:
                # Parse the frame content into a more readable format
                lines = frame_content.strip().split(',\\n')
                processed_lines = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Handle lists inside frame
                    if '[' in line and ']' in line:
                        key, value = line.split(':', 1)
                        processed_lines.append(f"{key.strip()}: {value.strip()}")
                    else:
                        processed_lines.append(line)
                
                # Create a text chunk from the frame
                text_chunk = f"Type: {frame_type}\\n" + "\\n".join(processed_lines)
                text_chunks.append(text_chunk)
            
            return text_chunks
            
        except Exception as e:
            logger.error(f"Error parsing Prolog file {file_path}: {str(e)}")
            return []
    
    def convert_prolog_to_chunks(self, prolog_files):
        """
        Convert multiple Prolog files to text chunks
        
        Args:
            prolog_files: List of Prolog file paths
            
        Returns:
            List of text chunks
        """
        all_chunks = []
        
        for file_path in prolog_files:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                continue
                
            chunks = self._parse_prolog_file(file_path)
            all_chunks.extend(chunks)
            logger.info(f"Extracted {len(chunks)} frames from {file_path}")
        
        return all_chunks
    
    def create_vector_store(self, text_chunks):
        """
        Create a vector store from text chunks
        
        Args:
            text_chunks: List of text chunks
            
        Returns:
            The created vector store
        """
        try:
            logger.info(f"Creating vector store with {len(text_chunks)} chunks")
            
            # Create vector store
            vectorstore = Chroma.from_texts(
                texts=text_chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # Persist the vector store
            vectorstore.persist()
            logger.info(f"Vector store created and persisted at {self.persist_directory}")
            
            return vectorstore
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            return None
    
    def process_all_knowledge_bases(self):
        """
        Process all Prolog knowledge bases and create a vector store
        
        Returns:
            The created vector store
        """
        # Check if we're running in Docker environment
        in_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)
        
        # Use appropriate paths based on environment
        if in_docker:
            logger.info("Running in Docker environment, using Docker paths")
            prolog_files = [
                '/app/knowledgebase_docker.pl',
                '/app/pea_updates_docker.pl',
                '/app/advanced_queries_docker.pl'
            ]
        else:
            logger.info("Running in local environment, using local paths")
            prolog_files = [
                'knowledgebase_docker.pl',
                'pea_updates_docker.pl',
                'advanced_queries_docker.pl'
            ]
        
        # Convert Prolog files to text chunks
        text_chunks = self.convert_prolog_to_chunks(prolog_files)
        
        if not text_chunks:
            logger.error("No text chunks extracted from Prolog files")
            return None
        
        # Create vector store
        return self.create_vector_store(text_chunks)
    
    def load_vector_store(self):
        """
        Load an existing vector store
        
        Returns:
            The loaded vector store
        """
        try:
            if os.path.exists(self.persist_directory):
                logger.info(f"Loading existing vector store from {self.persist_directory}")
                vectorstore = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory
                )
                return vectorstore
            else:
                logger.warning(f"No existing vector store found at {self.persist_directory}")
                return None
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None

class RAGQuery:
    """
    Query the RAG system with natural language queries
    """
    
    def __init__(self, vector_store):
        """
        Initialize the RAG query system
        
        Args:
            vector_store: Vector store to query
        """
        self.vector_store = vector_store
    
    def query(self, query_text, k=3):
        """
        Query the RAG system
        
        Args:
            query_text: Natural language query
            k: Number of results to return
            
        Returns:
            List of relevant text chunks
        """
        try:
            # Get similar documents
            docs = self.vector_store.similarity_search(query_text, k=k)
            
            # Extract content from documents
            results = [doc.page_content for doc in docs]
            
            return results
        except Exception as e:
            logger.error(f"Error querying RAG system: {str(e)}")
            return []

def get_rag_system():
    """
    Get or create a RAG system instance
    
    Returns:
        RAGQuery instance
    """
    try:
        # Initialize the converter with persistence directory from environment
        persist_dir = os.environ.get('RAG_PERSIST_DIR', './data/chromadb')
        converter = PrologToRAGConverter(persist_directory=persist_dir)
        
        # Try to load existing vector store
        vector_store = converter.load_vector_store()
        
        # If not found, create a new one
        if vector_store is None:
            vector_store = converter.process_all_knowledge_bases()
        
        # If we have a vector store, return a RAG query system
        if vector_store:
            return RAGQuery(vector_store)
        else:
            logger.error("Failed to create or load RAG system")
            return None
    except Exception as e:
        logger.error(f"Error creating RAG system: {str(e)}")
        return None

# For direct use in HybridEngine
def extend_hybrid_engine(hybrid_engine):
    """
    Extend HybridEngine with RAG capabilities
    
    Args:
        hybrid_engine: The HybridEngine instance to extend
    """
    if not hasattr(hybrid_engine, '_original_process_general_query'):
        # Store the original method
        hybrid_engine._original_process_general_query = hybrid_engine._process_general_query
        
        # Create RAG system
        hybrid_engine.rag_system = get_rag_system()
        
        # Replace the general query method
        def enhanced_process_general_query(self, params, attempt_ollama_call):
            """Enhanced version of _process_general_query that incorporates RAG"""
            logger.info("Using RAG-enhanced _process_general_query")
            
            # Get the query
            user_query = params.get("query", "") or params.get("message", "")
            
            if not user_query:
                return {
                    "response": "I couldn't understand your query. Please provide a clearer question.",
                    "source": "error_no_query"
                }
            
            # Try RAG if available
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"Querying RAG system with: {user_query}")
                    rag_results = self.rag_system.query(user_query)
                    
                    if rag_results:
                        # Format RAG results
                        combined_result = "Based on our knowledge base:\\n\\n" + "\\n\\n".join(rag_results)
                        return {"response": combined_result, "source": "rag"}
                    else:
                        logger.info("RAG system returned no results")
                except Exception as e:
                    logger.error(f"Error querying RAG system: {str(e)}")
            
            # Fall back to original method
            return self._original_process_general_query(params, attempt_ollama_call)
        
        # Bind the new method to the hybrid_engine
        hybrid_engine._process_general_query = enhanced_process_general_query.__get__(hybrid_engine)
        
        logger.info("Successfully enhanced HybridEngine with RAG capabilities")
    else:
        logger.info("HybridEngine already enhanced with RAG capabilities")

if __name__ == "__main__":
    # Example usage
    converter = PrologToRAGConverter()
    vector_store = converter.process_all_knowledge_bases()
    
    if vector_store:
        # Create the RAG query system
        rag_system = RAGQuery(vector_store)
        
        # Example query
        query = "How do I control aphids on peas?"
        results = rag_system.query(query)
        
        print(f"Query: {query}")
        print("Results:")
        for i, result in enumerate(results, 1):
            print(f"Result {i}:\\n{result}\\n")
'''
    return content

def create_initialize_rag():
    """Create the initialize_rag.py file."""
    content = '''#!/usr/bin/env python
"""
Script to initialize RAG system during container startup.
"""
import os
import logging
import sys

# Configure logging with proper format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("rag_initializer")

def initialize_rag():
    """Initialize the RAG system with the knowledge base."""
    logger.info("Starting RAG initialization...")
    
    try:
        logger.info("Checking environment variables...")
        rag_enabled = os.environ.get("USE_RAG", "false").lower() == "true"
        
        if not rag_enabled:
            logger.info("RAG initialization skipped: USE_RAG is not set to 'true'")
            return False
        
        persist_dir = os.environ.get("RAG_PERSIST_DIR")
        if not persist_dir:
            logger.warning("RAG_PERSIST_DIR not set, using default './data/chromadb'")
            persist_dir = "./data/chromadb"
        
        logger.info(f"Using persistence directory: {persist_dir}")
        
        # Import the RAG converter
        logger.info("Importing RAG components...")
        from api.inference_engine.implement_rag import PrologToRAGConverter
        
        # Initialize the converter
        logger.info("Initializing PrologToRAGConverter...")
        converter = PrologToRAGConverter(persist_directory=persist_dir)
        
        # Check if vector store already exists
        logger.info("Checking for existing vector store...")
        vector_store = converter.load_vector_store()
        
        if vector_store:
            logger.info("Existing vector store found and loaded successfully")
            return True
        
        # Process the knowledge base and create vector store
        logger.info("Creating new vector store from knowledge base...")
        vector_store = converter.process_all_knowledge_bases()
        
        if vector_store:
            logger.info("Vector store created successfully")
            return True
        else:
            logger.error("Failed to create vector store")
            return False
            
    except ImportError as e:
        logger.error(f"Import error: {str(e)}. Make sure RAG dependencies are installed.")
        return False
    except Exception as e:
        logger.error(f"Error initializing RAG: {str(e)}")
        return False

if __name__ == "__main__":
    success = initialize_rag()
    
    if success:
        logger.info("RAG initialization completed successfully")
        sys.exit(0)
    else:
        logger.error("RAG initialization failed")
        # Exit with success code anyway to not block container startup
        sys.exit(0)
'''
    return content

def modify_start_web_script():
    """Modify the start_web.sh script to initialize RAG."""
    if not os.path.exists(START_WEB_SCRIPT):
        logger.error(f"start_web.sh script not found: {START_WEB_SCRIPT}")
        return False
    
    # Backup the original file
    backup_path = f"{START_WEB_SCRIPT}.bak"
    if not os.path.exists(backup_path):
        shutil.copy2(START_WEB_SCRIPT, backup_path)
        logger.info(f"Created backup of {START_WEB_SCRIPT} as {backup_path}")
    
    try:
        with open(START_WEB_SCRIPT, 'r') as f:
            content = f.read()
        
        # Check if RAG initialization is already added
        if "Initialize RAG" in content:
            logger.info("RAG initialization already added to start_web.sh")
            return True
        
        # Prepare RAG initialization code
        rag_init_code = """
# Initialize RAG if enabled
if [ "$USE_RAG" = "true" ]; then
    echo "======================================"
    echo "Initializing RAG system..."
    echo "======================================"
    
    # Create data directory if it doesn't exist
    if [ ! -d "$RAG_PERSIST_DIR" ]; then
        echo "Creating directory: $RAG_PERSIST_DIR"
        mkdir -p "$RAG_PERSIST_DIR"
    fi
    
    # Run the initialization script
    python /app/initialize_rag.py
    
    # Check exit code
    if [ $? -eq 0 ]; then
        echo "RAG initialization completed"
    else
        echo "WARNING: RAG initialization encountered issues, but continuing startup"
    fi
    
    echo "======================================"
fi
"""
        
        # Find a good insertion point - before Django server starts
        patterns = ["python manage.py runserver", "gunicorn", "uwsgi", "#!/bin/bash"]
        
        insert_pos = None
        for pattern in patterns:
            if pattern in content:
                if pattern == "#!/bin/bash":
                    # Insert after the shebang
                    insert_pos = content.find(pattern) + len(pattern)
                else:
                    # Insert before the server start command
                    insert_pos = content.find(pattern)
                break
        
        if insert_pos is not None:
            new_content = content[:insert_pos] + rag_init_code + content[insert_pos:]
        else:
            # If no suitable insertion point found, append to the end
            new_content = content.rstrip() + "\n\n" + rag_init_code
        
        # Write the updated script
        with open(START_WEB_SCRIPT, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Updated {START_WEB_SCRIPT} with RAG initialization code")
        return True
    
    except Exception as e:
        logger.error(f"Error modifying {START_WEB_SCRIPT}: {str(e)}")
        return False

def update_docker_compose():
    """Update docker-compose.yml to add RAG configuration."""
    if not os.path.exists(DOCKER_COMPOSE_PATH):
        logger.error(f"docker-compose.yml not found: {DOCKER_COMPOSE_PATH}")
        return False
    
    # Make a backup of the original file
    backup_path = f"{DOCKER_COMPOSE_PATH}.bak"
    if not os.path.exists(backup_path):
        shutil.copy2(DOCKER_COMPOSE_PATH, backup_path)
        logger.info(f"Created backup of {DOCKER_COMPOSE_PATH} as {backup_path}")
    
    try:
        # Read the current docker-compose.yml
        with open(DOCKER_COMPOSE_PATH, 'r') as f:
            config = yaml.safe_load(f)
        
        # Add chroma_data volume if not exists
        if 'volumes' in config and 'chroma_data' not in config['volumes']:
            config['volumes']['chroma_data'] = None
            logger.info("Added chroma_data volume to docker-compose.yml")
        
        # Update web service
        if 'services' in config and 'web' in config['services']:
            web_service = config['services']['web']
            
            # Add chroma volume mount
            if 'volumes' in web_service:
                volume_mount = 'chroma_data:/app/data/chromadb'
                if volume_mount not in web_service['volumes']:
                    web_service['volumes'].append(volume_mount)
                    logger.info(f"Added {volume_mount} to web service volumes")
            
            # Add environment variables
            if 'environment' in web_service:
                # Define RAG environment variables
                rag_env_vars = {
                    'USE_RAG': 'true',
                    'RAG_PERSIST_DIR': '/app/data/chromadb'
                }
                
                # Handle both list and dict formats
                if isinstance(web_service['environment'], list):
                    # List format (like ["VAR=value", "VAR2=value2"])
                    for key, value in rag_env_vars.items():
                        env_var = f"{key}={value}"
                        if env_var not in web_service['environment']:
                            web_service['environment'].append(env_var)
                            logger.info(f"Added {env_var} to web service environment")
                else:
                    # Dict format (like {VAR: value, VAR2: value2})
                    for key, value in rag_env_vars.items():
                        if key not in web_service['environment']:
                            web_service['environment'][key] = value
                            logger.info(f"Added {key}={value} to web service environment")
        
        # Write updated docker-compose.yml
        with open(DOCKER_COMPOSE_PATH, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        logger.info(f"Successfully updated {DOCKER_COMPOSE_PATH}")
        return True
    
    except Exception as e:
        logger.error(f"Error updating {DOCKER_COMPOSE_PATH}: {str(e)}")
        return False

def update_requirements():
    """Update requirements to include RAG dependencies."""
    requirements_txt = os.path.join(APP_DIR, "requirements.txt")
    if not os.path.exists(requirements_txt):
        logger.error(f"requirements.txt not found: {requirements_txt}")
        return False
    
    # RAG dependencies
    rag_requirements = """
# RAG dependencies
langchain==0.1.8
langchain-community==0.0.19
chromadb==0.4.24
sentence-transformers==2.5.1
huggingface-hub==0.20.3
pysbd==0.3.4
regex==2023.12.25
"""
    
    # Backup the original file
    backup_path = f"{requirements_txt}.bak"
    if not os.path.exists(backup_path):
        shutil.copy2(requirements_txt, backup_path)
        logger.info(f"Created backup of {requirements_txt} as {backup_path}")
    
    try:
        with open(requirements_txt, 'r') as f:
            content = f.read()
        
        # Check if RAG dependencies already exist
        if "langchain" in content and "chromadb" in content:
            logger.info("RAG dependencies already present in requirements.txt")
            return True
        
        # Add RAG dependencies
        with open(requirements_txt, 'a') as f:
            f.write(rag_requirements)
        
        logger.info(f"Added RAG dependencies to {requirements_txt}")
        return True
    
    except Exception as e:
        logger.error(f"Error updating {requirements_txt}: {str(e)}")
        return False

def update_hybrid_engine_init():
    """Modify __init__.py to initialize RAG for HybridEngine."""
    init_py = os.path.join(INFERENCE_ENGINE_DIR, "__init__.py")
    
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(init_py), exist_ok=True)
    
    # Check if file exists and create backup if it does
    if os.path.exists(init_py):
        backup_path = f"{init_py}.bak"
        if not os.path.exists(backup_path):
            shutil.copy2(init_py, backup_path)
            logger.info(f"Created backup of {init_py} as {backup_path}")
        
        # Read existing content
        try:
            with open(init_py, 'r') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading {init_py}: {str(e)}")
            content = ""
    else:
        content = "# Inference Engine initialization\n"
    
    # Check if RAG initialization is already added
    if "RAG" in content and "extend_hybrid_engine" in content:
        logger.info("RAG initialization already present in __init__.py")
        return True
    
    # Prepare RAG initialization code
    rag_init_code = """
# Initialize RAG integration if enabled
import os

# Apply RAG integration to HybridEngine
if os.environ.get('USE_RAG', 'false').lower() == 'true':
    try:
        from api.inference_engine.hybrid_engine import HybridEngine
        from api.inference_engine.implement_rag import extend_hybrid_engine
        
        # Get or create the HybridEngine instance
        try:
            # Try to get the singleton instance if available
            from api.inference_engine import hybrid_engine
            engine = hybrid_engine
            print("Found existing HybridEngine instance, extending with RAG")
        except (ImportError, AttributeError):
            # Create a new instance if needed
            engine = HybridEngine()
            print("Created new HybridEngine instance, extending with RAG")
        
        # Extend the engine with RAG capabilities
        extend_hybrid_engine(engine)
        print("Successfully extended HybridEngine with RAG capabilities")
    except Exception as e:
        import logging
        logging.error(f"Error integrating RAG with HybridEngine: {str(e)}")
        print(f"Error integrating RAG with HybridEngine: {str(e)}")
"""
    
    # Add RAG initialization code
    new_content = content.rstrip() + "\n\n" + rag_init_code
    
    try:
        with open(init_py, 'w') as f:
            f.write(new_content)
        logger.info(f"Updated {init_py} with RAG initialization code")
        return True
    except Exception as e:
        logger.error(f"Error updating {init_py}: {str(e)}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = [
        INFERENCE_ENGINE_DIR,  # /api/inference_engine/
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"Created directory: {directory}")
            except Exception as e:
                logger.error(f"Error creating directory {directory}: {str(e)}")

def create_files():
    """Create necessary files."""
    files_content = {
        source_files["implement_rag.py"]: create_implement_rag(),
        source_files["initialize_rag.py"]: create_initialize_rag(),
    }
    
    for file_path, content in files_content.items():
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Create file
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"Created file: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {str(e)}")

def setup_rag():
    """Set up RAG integration."""
    logger.info("=== Setting up RAG integration ===")
    
    # 1. Create necessary directories
    logger.info("Creating directories...")
    create_directories()
    
    # 2. Create implementation files
    logger.info("Creating implementation files...")
    create_files()
    
    # 3. Update Docker configuration
    logger.info("Updating docker-compose.yml...")
    update_docker_compose()
    
    # 4. Add RAG dependencies to requirements.txt
    logger.info("Updating requirements.txt...")
    update_requirements()
    
    # 5. Modify start_web.sh to initialize RAG
    logger.info("Updating start_web.sh...")
    modify_start_web_script()
    
    # 6. Update HybridEngine initialization
    logger.info("Setting up HybridEngine initialization...")
    update_hybrid_engine_init()
    
    logger.info("=== RAG setup completed successfully ===")
    logger.info("\nNext steps:")
    logger.info("1. Review the changes")
    logger.info("2. Rebuild the Docker container: docker-compose build web")
    logger.info("3. Restart the services: docker-compose up -d")
    logger.info("4. Check the logs: docker-compose logs -f web")

if __name__ == "__main__":
    setup_rag() 