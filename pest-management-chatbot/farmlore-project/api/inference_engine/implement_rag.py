import os
import logging
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import re
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper to find the value of a key in frame lines (e.g., name: value,)
def _get_value_from_frame_lines(frame_lines, key):
    for line in frame_lines:
        line = line.strip()
        if line.startswith(key + ':'):
            value_part = line[len(key + ':'):].strip()
            if value_part.endswith(','):
                value_part = value_part[:-1].strip()
            
            # Handle lists like symptoms: [item1, item2]
            if value_part.startswith('[') and value_part.endswith(']'):
                # Extract elements from list, stripping quotes and whitespace
                elements_str = value_part[1:-1]
                # Split by comma, but be careful about commas within quotes (not handled perfectly here)
                elements = [el.strip().strip("'\"") for el in elements_str.split(',') if el.strip()]
                return elements
            # Handle single values
            return value_part.strip().strip("'\"")
    return None

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
            self.persist_directory = os.environ.get('RAG_PERSIST_DIR', './data/chromadb_improved')
        else:
            self.persist_directory = persist_directory
            
        logger.info(f"Using persistence directory: {self.persist_directory}")
        
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Create the persist directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        logger.info(f"PrologToRAGConverter initialized. Embeddings: {embedding_model}, Persist Dir: {self.persist_directory}")
    
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
            
            logger.debug(f"Read {len(text_chunks)} lines from {file_path}")
            return text_chunks
            
        except FileNotFoundError:
            logger.error(f"Prolog file not found: {file_path}")
            return []
    
    def _group_lines_into_frames(self, content_lines):
        frames = []
        current_frame_lines = []
        in_frame_block = False # Tracks if we are inside a frame(...) block

        for line_num, line_content in enumerate(content_lines):
            stripped_line = line_content.strip()

            if not stripped_line or stripped_line.startswith('%') or stripped_line.startswith(':-'):
                # If we encounter a comment/directive and were in a frame, end the current frame.
                if in_frame_block and current_frame_lines:
                    frames.append(current_frame_lines)
                    current_frame_lines = []
                in_frame_block = False
                continue

            # Detect start of a new frame block
            if stripped_line.lower().startswith('frame('):
                if in_frame_block and current_frame_lines: # End previous frame
                    frames.append(current_frame_lines)
                
                # Start new frame, remove 'frame(' prefix
                # And if it's a single line frame like frame(type, [...]). then handle it
                if stripped_line.endswith(']).'):
                    # Single line frame
                    frame_content_part = stripped_line[len('frame('):-3] # Remove frame(...) and ]).
                    frames.append([frame_content_part.strip()])
                    in_frame_block = False # Frame ended
                    current_frame_lines = []
                else:
                    current_frame_lines = [stripped_line[len('frame('):]]
                    in_frame_block = True
            elif in_frame_block:
                # Continue collecting lines for the current frame
                # Detect end of frame block by ']).'
                if stripped_line.endswith(']).'):
                    current_frame_lines.append(stripped_line[:-3].strip()) # Remove ']).'
                    if current_frame_lines: # Add if not empty
                        frames.append(current_frame_lines)
                    current_frame_lines = []
                    in_frame_block = False
                else:
                    current_frame_lines.append(stripped_line)
            # else:
                # Lines not part of a frame (e.g. plain facts, though KB uses frames)
                # logger.debug(f"Line outside frame: {stripped_line}")
                # frames.append([stripped_line]) # Treat as a single-line "frame" for processing

        if in_frame_block and current_frame_lines: # Add any trailing frame being built
            frames.append(current_frame_lines)
        
        # logger.debug(f"Grouped into {len(frames)} frames. First frame (sample): {frames[0] if frames else 'N/A'}")
        return frames

    def _process_frame_for_rag(self, frame_lines):
        # frame_lines is a list of strings, each being a content line from a frame(...) definition
        # e.g., ["name: aphid_general,", "type: insect,", "symptoms: [symptom1, symptom2],"]
        
        texts = []
        # Attempt to get a primary identifier for the frame, usually 'name'
        # This helper needs to be robust to variations in line endings (comma or not)
        subject_name = _get_value_from_frame_lines(frame_lines, 'name')
        frame_type = _get_value_from_frame_lines(frame_lines, 'type')

        if not subject_name:
            # Fallback for simple lines or frames without a clear 'name' slot
            # This ensures that lines not conforming to typical frame structure are still processed
            processed_lines = []
            for line in frame_lines:
                clean_line = line.strip().rstrip(',').rstrip('.')
                if clean_line:
                    processed_lines.append(clean_line)
            if processed_lines:
                texts.append("General information: " + "; ".join(processed_lines))
            # logger.debug(f"Processing frame with no subject_name. Lines: {frame_lines}, Generated text: {texts}")
            return list(set(filter(None, texts)))

        # General description for the frame subject
        base_info = f"Regarding '{subject_name}'"
        if frame_type:
            base_info += f" (a type of {frame_type})"
        
        texts.append(f"{base_info}:")

        # Process known complex slots like symptoms, monitoring, controls by itemizing them
        for slot_key in ['symptoms', 'monitoring', 'controls', 'pests', 'diseases', 'resolves']:
            slot_values = _get_value_from_frame_lines(frame_lines, slot_key)
            if slot_values and isinstance(slot_values, list):
                for item in slot_values:
                    item_text = item.strip()
                    if item_text:
                        # Make the text more contextual
                        if slot_key == 'symptoms':
                            texts.append(f"A symptom of '{subject_name}' is: {item_text}.")
                            texts.append(f"'{subject_name}' can cause: {item_text}.")
                        elif slot_key == 'monitoring':
                            texts.append(f"Monitoring for '{subject_name}' includes: {item_text}.")
                        elif slot_key == 'controls':
                            texts.append(f"A control method for '{subject_name}' is: {item_text}.")
                        elif slot_key == 'pests' and frame_type == 'crop':
                            texts.append(f"The crop '{subject_name}' can be affected by the pest: {item_text}.")
                        elif slot_key == 'diseases' and frame_type == 'crop':
                             texts.append(f"The crop '{subject_name}' is susceptible to the disease: {item_text}.")
                        elif slot_key == 'resolves' and frame_type == 'practice':
                             texts.append(f"The practice '{subject_name}' can help resolve: {item_text}.")
                        else: # Generic itemization
                            texts.append(f"For '{subject_name}', a {slot_key.rstrip('s')} detail is: {item_text}.")


        # Add other simple key-value pairs as descriptive text
        for line in frame_lines:
            line = line.strip().rstrip(',') # Clean trailing comma
            if ':' in line:
                key, value_part = line.split(':', 1)
                key = key.strip()
                value = value_part.strip().strip("'\"") # Strip quotes

                # Avoid reprocessing already itemized complex slots or the main identifiers
                if key not in ['name', 'type', 'symptoms', 'monitoring', 'controls', 'pests', 'diseases', 'resolves'] and value and value != "[]" and value != "''":
                    # Ensure value is not a list representation itself, as those are handled above
                    if not (value.startswith('[') and value.endswith(']')):
                        texts.append(f"Details for '{subject_name}': {key} is {value}.")
        
        # logger.debug(f"Processed frame for '{subject_name}'. Generated texts (sample): {texts[:3] if texts else 'None'}")
        # Deduplicate and filter empty strings
        return list(set(filter(None, texts)))

    def convert_prolog_to_chunks(self, prolog_files):
        """
        Converts Prolog files into a list of text chunks (Documents).
        Each frame is processed into one or more descriptive text chunks.
        """
        all_prolog_data = {}
        for file_path in prolog_files:
            lines = self._parse_prolog_file(file_path)
            if lines:
                all_prolog_data[file_path] = lines
        
        all_extracted_texts = []
        for file_path, content_lines in all_prolog_data.items():
            logger.info(f"Grouping and processing frames from {file_path} for RAG...")
            
            frames = self._group_lines_into_frames(content_lines)
            file_texts = []
            for frame_idx, frame_lines in enumerate(frames):
                # logger.debug(f"Processing frame {frame_idx+1}/{len(frames)} from {file_path} with {len(frame_lines)} lines.")
                processed_texts = self._process_frame_for_rag(frame_lines)
                if processed_texts:
                    file_texts.extend(processed_texts)
            
            if file_texts:
                logger.info(f"Extracted {len(file_texts)} text snippets from {file_path}")
                all_extracted_texts.extend(file_texts)
            else:
                logger.warning(f"No text snippets extracted from {file_path}")

        # Create Langchain Document objects from the extracted texts
        documents = [Document(page_content=text) for text in all_extracted_texts]
        logger.info(f"Created {len(documents)} Document objects for RAG from all Prolog files.")
        
        # Optional: Further split large documents if any single processed text is too long
        # For now, assuming _process_frame_for_rag generates reasonably sized chunks.
        # If not, text_splitter can be used here on `documents`.
        # Example: docs_for_store = self.text_splitter.split_documents(documents)

        return documents # Return the list of Document objects

    def _extract_text_from_prolog_content(self, prolog_content_lines):
        # This method is now effectively replaced by _group_lines_into_frames and _process_frame_for_rag
        # Kept for compatibility or if a simpler line-by-line extraction is needed elsewhere.
        # However, convert_prolog_to_chunks should be the primary user of the new frame-based logic.
        logger.warning("_extract_text_from_prolog_content is deprecated for main RAG pipeline; frame processing is used.")
        extracted_texts = []
        # ... existing code ...
        return extracted_texts

    def create_vector_store(self, text_chunks_docs): # Expects list of Document objects
        """
        Creates a ChromaDB vector store from text chunks (Langchain Document objects).
        """
        if not text_chunks_docs: # Changed variable name for clarity
            logger.warning("No text chunks provided to create vector store.")
            return None
        try:
            logger.info(f"Creating new vector store in {self.persist_directory} with {len(text_chunks_docs)} documents.") # Changed variable name
            # Ensure text_chunks_docs are actual Document objects, not just strings
            if text_chunks_docs and not isinstance(text_chunks_docs[0], Document):
                 logger.error("text_chunks_docs must be a list of Langchain Document objects.")
                 return None

            vector_store = Chroma.from_documents(
                documents=text_chunks_docs, # Changed variable name
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info(f"Vector store created and persisted to {self.persist_directory}.")
            return vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}", exc_info=True) # Added exc_info
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
                '/app/prolog_integration/knowledgebase.pl',
                '/app/prolog_integration/pea_updates.pl',
                '/app/prolog_integration/advanced_queries.pl'
            ]
        else:
            logger.info("Running in local environment, using local paths relative to project root")
            # Assuming the script is run from pest-management-chatbot/farmlore-project/
            # or that the current working directory is set appropriately for local execution.
            # These paths might need adjustment for local non-Docker runs depending on CWD.
            base_dir = os.path.join(os.getcwd(), "prolog_integration") if not os.path.exists("prolog_integration") else "prolog_integration"
            
            # A more robust way for local paths if this script can be called from different locations
            # would be to determine the project root dynamically or use absolute paths for local dev.
            # For now, assuming a common local execution setup.
            # If this script (implement_rag.py) is in api/inference_engine/, 
            # then prolog_integration is ../../prolog_integration
            script_dir = os.path.dirname(os.path.abspath(__file__))
            local_prolog_dir = os.path.join(script_dir, "..", "..", "prolog_integration")

            prolog_files = [
                os.path.join(local_prolog_dir, 'knowledgebase.pl'),
                os.path.join(local_prolog_dir, 'pea_updates.pl'),
                os.path.join(local_prolog_dir, 'advanced_queries.pl')
            ]
            logger.info(f"Constructed local paths: {prolog_files}")
        
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
        if not self.vector_store:
            logger.error("RAGQuery initialized with no vector store!")
    
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
            # Ensure vector_store is not None before calling similarity_search
            if not self.vector_store:
                logger.error("Cannot query RAG: Vector store is not available.")
                return []
            
            docs = self.vector_store.similarity_search(query_text, k=k)
            logger.debug(f"RAG similarity_search returned {len(docs)} documents for query: '{query_text}'")
            
            # Extract content from documents
            results = [doc.page_content for doc in docs]
            
            return results
        except Exception as e:
            logger.error(f"Error querying RAG system: {str(e)}")
            return []

def get_rag_system():
    """
    Get or create a RAG system instance. This will now trigger the new processing logic.
    """
    try:
        # Initialize the converter with persistence directory from environment
        persist_dir = os.environ.get('RAG_PERSIST_DIR', './data/chromadb_improved') # Use new default/env var
        converter = PrologToRAGConverter(persist_directory=persist_dir)
        
        # Try to load existing vector store
        # For development, always recreate if logic changes:
        # if os.path.exists(persist_dir):
        #    logger.info(f"Deleting existing persist_dir for testing: {persist_dir}")
        #    import shutil
        #    shutil.rmtree(persist_dir)

        vector_store = converter.load_vector_store()
        
        # If not found, or if we want to force re-creation for testing
        if vector_store is None: # or FORCE_RECREATE_RAG_DB:
            logger.info("No existing vector store found or recreation forced. Processing knowledge bases...")
            vector_store = converter.process_all_knowledge_bases()
        else:
            logger.info(f"Loaded existing vector store from {persist_dir}")
        
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
                logger.info(f"RAG_EXTEND: Using RAG-enhanced {target_method}")
                
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
                
                logger.info(f"RAG_EXTEND: Extracted query: {query}")
                
                # If we found a query, try RAG
                if query and self.rag_system:
                    try:
                        logger.info(f"RAG_EXTEND: Querying RAG vector store with: '{query}'")
                        rag_results = self.rag_system.query(query)
                        logger.info(f"RAG_EXTEND: RAG vector store results: {rag_results}")
                        
                        if rag_results:
                            context = "\n\n".join(rag_results)
                            logger.info(f"RAG_EXTEND: RAG context prepared, {len(context)} characters.")
                            
                            # Use the context with Ollama if available
                            if hasattr(self, 'ollama_handler') and self.ollama_handler:
                                logger.info("RAG_EXTEND: Ollama handler found, attempting to use RAG context with Ollama.")
                                ollama_prompt = f"""Based on the following information from our knowledge base, 
answer the user's question: {query}

KNOWLEDGE BASE INFORMATION:
{context}

Answer with detailed, accurate information from the knowledge base. If the knowledge base doesn't contain 
information to answer the question, say so and provide general advice."""
                                logger.info(f"RAG_EXTEND: Constructed Ollama prompt with RAG context:\n{ollama_prompt}")
                                
                                response = self.ollama_handler.generate_response(ollama_prompt)
                                logger.info(f"RAG_EXTEND: Response from Ollama after RAG context injection: {response}")
                                return {"response": response, "source": "rag_ollama_dynamic_ctxt"}
                                
                            # Add context to return value if possible
                            if 'response' in kwargs:
                                logger.info(f"RAG_EXTEND: Ollama handler not used directly here, appending RAG context to original method's potential response.")
                                kwargs['response'] += f"\n\nAdditional information from RAG:\n{context}"
                    except Exception as e:
                        logger.error(f"RAG_EXTEND: Error using RAG: {str(e)}")
                
                # Call original method
                logger.info(f"RAG_EXTEND: Calling original method _original_{target_method}")
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