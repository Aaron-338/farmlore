import os
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
                lines = frame_content.strip().split(',\n')
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
                text_chunk = f"Type: {frame_type}\n" + "\n".join(processed_lines)
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
    try:
        logger.info("Extending HybridEngine with RAG capabilities...")
        
        # Create RAG system
        hybrid_engine.rag_system = get_rag_system()
        
        if not hybrid_engine.rag_system:
            logger.error("Failed to create RAG system")
            return
        
        # Log all methods to help with debugging
        method_list = [m for m in dir(hybrid_engine) if not m.startswith('_') and callable(getattr(hybrid_engine, m))]
        logger.info(f"Available methods in HybridEngine: {method_list}")
        
        # Docker integration: Try to detect the specific query method to patch
        docker_query_methods = ['process_query', '_process_general_query', '_process_query', 
                               'process_general_query', 'query', 'handle_query']
        
        target_method = None
        for method_name in docker_query_methods:
            if hasattr(hybrid_engine, method_name):
                target_method = method_name
                logger.info(f"Found query method to patch: {method_name}")
                break
        
        if target_method:
            # Store the original method
            setattr(hybrid_engine, f"_original_{target_method}", getattr(hybrid_engine, target_method))
            logger.info(f"Stored original method as _original_{target_method}")
            
            # Define the enhanced method
            def enhanced_query_method(self, *args, **kwargs):
                """Enhanced version of query method that incorporates RAG"""
                logger.info(f"Using RAG-enhanced {target_method}")
                
                # Try to get query from args or kwargs
                query = None
                params = None
                
                # Handle different method signatures
                if args and len(args) > 0:
                    if isinstance(args[0], str):
                        # If first arg is string, it's probably the query
                        query = args[0]
                    elif isinstance(args[0], dict):
                        # If first arg is dict, it's probably params
                        params = args[0]
                        query = params.get("query", "") or params.get("message", "")
                
                # Try to get query from kwargs
                if not query and 'query' in kwargs:
                    query = kwargs['query']
                if not query and 'message' in kwargs:
                    query = kwargs['message']
                    
                # For two-arg case where first is query_type and second is params
                if not query and len(args) >= 2 and isinstance(args[1], dict):
                    params = args[1]
                    query = params.get("query", "") or params.get("message", "")
                
                logger.info(f"Extracted query: {query}")
                
                # If we found a query, try RAG
                if query and self.rag_system:
                    try:
                        logger.info(f"Querying RAG system with: {query}")
                        rag_results = self.rag_system.query(query)
                        
                        if rag_results:
                            context = "\n\n".join(rag_results)
                            logger.info(f"RAG context found, {len(context)} characters")
                            
                            # Use the context with Ollama if available
                            if hasattr(self, 'ollama_handler') and self.ollama_handler:
                                logger.info("Using RAG context with Ollama...")
                                ollama_prompt = f"""Based on the following information from our knowledge base, 
answer the user's question: {query}

KNOWLEDGE BASE INFORMATION:
{context}

Answer with detailed, accurate information from the knowledge base. If the knowledge base doesn't contain 
information to answer the question, say so and provide general advice."""
                                
                                response = self.ollama_handler.generate_response(ollama_prompt)
                                return {"response": response, "source": "rag_ollama"}
                                
                            # Add context to return value if possible
                            if 'response' in kwargs:
                                kwargs['response'] += f"\n\nAdditional information:\n{context}"
                    except Exception as e:
                        logger.error(f"Error using RAG: {str(e)}")
                
                # Call original method
                original_method = getattr(self, f"_original_{target_method}")
                return original_method(*args, **kwargs)
            
            # Bind the enhanced method
            import types
            setattr(hybrid_engine, target_method, types.MethodType(enhanced_query_method, hybrid_engine))
            logger.info(f"Successfully patched {target_method} with RAG capabilities")
            
        else:
            # Fallback: Try to find any method that might handle queries
            logger.warning("Could not find standard query method, searching for alternatives...")
            
            potential_handlers = [m for m in method_list if any(x in m.lower() for x in 
                                ['query', 'process', 'pest', 'management', 'chat', 'handle', 'respond'])]
            
            if potential_handlers:
                logger.info(f"Found potential handlers: {potential_handlers}")
                # We'll just attach the RAG system and let it be used manually
                logger.info("Attaching RAG system to HybridEngine for manual use")
            else:
                logger.warning("No suitable query methods found, RAG will be available but may not be used automatically")
        
        logger.info("HybridEngine extended with RAG capabilities")
        return True
    except Exception as e:
        logger.error(f"Error extending HybridEngine with RAG: {str(e)}")
        return False

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
            print(f"Result {i}:\n{result}\n") 