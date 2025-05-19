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
                        combined_result = "Based on our knowledge base:\n\n" + "\n\n".join(rag_results)
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
            print(f"Result {i}:\n{result}\n")
