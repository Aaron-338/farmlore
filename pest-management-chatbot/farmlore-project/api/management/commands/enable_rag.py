"""
Django management command to enable RAG in the system.
"""

from django.core.management.base import BaseCommand
import os
import sys
import logging
import types
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Enable RAG for the Pest Management Chatbot'
    
    def handle(self, *args, **options):
        self.stdout.write("Enabling RAG for the Pest Management Chatbot...")
        
        # Set RAG environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Create the ChromaDB directory if it doesn't exist
        os.makedirs(os.environ['RAG_PERSIST_DIR'], exist_ok=True)
        
        # Get the HybridEngine instance
        try:
            from api.inference_engine.hybrid_engine import hybrid_engine
            self.stdout.write(self.style.SUCCESS("✓ Found HybridEngine instance"))
        except ImportError:
            self.stdout.write(self.style.ERROR("⚠ Could not import hybrid_engine"))
            return
        
        # Check if we already have a RAG system
        if hasattr(hybrid_engine, 'rag_system'):
            self.stdout.write(self.style.SUCCESS("✓ RAG system is already attached to HybridEngine"))
        else:
            # Import RAG modules
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                from langchain_community.vectorstores import Chroma
            except ImportError:
                self.stdout.write(self.style.WARNING("⚠ Failed to import LangChain modules. Installing..."))
                try:
                    import subprocess
                    subprocess.run(["pip", "install", "langchain", "langchain-community", "sentence-transformers", "chromadb"])
                    from langchain_community.embeddings import HuggingFaceEmbeddings
                    from langchain_community.vectorstores import Chroma
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"⚠ Failed to install dependencies: {str(e)}"))
                    return
            
            # Create a simple RAG class for direct integration
            class SimpleRAG:
                def __init__(self, persist_dir):
                    self.persist_dir = persist_dir
                    self.stdout.write("Initializing embeddings model...")
                    self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                    
                    if os.path.exists(persist_dir) and os.path.isdir(persist_dir) and any(os.listdir(persist_dir)):
                        self.stdout.write(f"Loading existing vector store from {persist_dir}")
                        self.vector_store = Chroma(
                            embedding_function=self.embeddings,
                            persist_directory=persist_dir
                        )
                    else:
                        self.stdout.write(f"Creating new vector store at {persist_dir}")
                        # Create a simple vector store with sample data about aphids
                        texts = [
                            "Ladybugs (Coccinellidae) are effective natural predators for aphids. They can consume up to 50-60 aphids per day.",
                            "Lacewings are voracious predators that feed on aphids. Both adults and larvae can consume large numbers of aphids.",
                            "Hoverflies lay their eggs near aphid colonies, and their larvae feed on the aphids.",
                            "Parasitic wasps lay their eggs inside aphids, and the larvae consume the aphids from the inside.",
                            "Predatory midges (Aphidoletes aphidimyza) specifically target aphids and can be very effective for aphid control."
                        ]
                        
                        self.vector_store = Chroma.from_texts(
                            texts=texts,
                            embedding=self.embeddings,
                            persist_directory=persist_dir
                        )
                        self.vector_store.persist()
                
                def query(self, query_text, k=3):
                    """Query the RAG system for relevant information"""
                    try:
                        docs = self.vector_store.similarity_search(query_text, k=k)
                        return [doc.page_content for doc in docs]
                    except Exception as e:
                        logger.error(f"Error querying RAG: {str(e)}")
                        return []
            
            # Add the stdout method to SimpleRAG
            SimpleRAG.stdout = self.stdout
            
            # Create and attach the RAG system
            self.stdout.write("Creating and attaching RAG system...")
            hybrid_engine.rag_system = SimpleRAG(os.environ['RAG_PERSIST_DIR'])
            self.stdout.write(self.style.SUCCESS("✓ RAG system created and attached to HybridEngine"))
        
        # Store the original query method
        if not hasattr(hybrid_engine, '_original_query'):
            hybrid_engine._original_query = hybrid_engine.query
            self.stdout.write(self.style.SUCCESS("✓ Stored original query method"))
        else:
            self.stdout.write(self.style.SUCCESS("✓ Original query method already stored"))
        
        # Create a wrapper around the query method to include RAG results
        def query_with_rag(self, query_type, params=None):
            """Wrap the query method to include RAG results"""
            logger.info(f"RAG-enhanced query called with type: {query_type}")
            
            if params is None:
                params = {}
            
            # Extract the query from params
            user_query = params.get("query", "") or params.get("message", "")
            
            # Check if this is a query type that could benefit from RAG
            if query_type in ["general", "general_query", "pest_management", "control_methods", "pest_identification"]:
                logger.info(f"Querying RAG system for: {user_query}")
                rag_results = self.rag_system.query(user_query)
                
                if rag_results:
                    logger.info(f"RAG found {len(rag_results)} relevant results")
                    # Get the original result
                    original_result = self._original_query(query_type, params)
                    
                    # Add RAG info to the response
                    rag_content = "Based on our knowledge base:\n\n" + "\n\n".join(rag_results)
                    
                    # If the original result has a response, combine it with RAG info
                    if isinstance(original_result, dict) and "response" in original_result:
                        if "predator" in user_query.lower() or "aphid" in user_query.lower():
                            # For predator queries, prioritize RAG results
                            original_result["response"] = rag_content + "\n\n" + original_result["response"]
                            original_result["source"] = "rag_combined"
                        else:
                            # For other queries, add RAG as additional info
                            original_result["response"] += "\n\nAdditional information from our knowledge base:\n" + rag_content
                            original_result["source"] = "hybrid_rag"
                        
                        return original_result
            
            # For non-RAG queries or if RAG found nothing, use the original method
            return self._original_query(query_type, params)
        
        # Replace the query method with our RAG-enhanced version
        hybrid_engine.query = types.MethodType(query_with_rag, hybrid_engine)
        self.stdout.write(self.style.SUCCESS("✓ Query method replaced with RAG-enhanced version"))
        
        # Test a simple query
        test_query = "What are natural predators for aphids?"
        self.stdout.write(f"\nTesting with query: '{test_query}'")
        test_result = hybrid_engine.rag_system.query(test_query)
        
        if test_result:
            self.stdout.write("\nRAG Results:")
            self.stdout.write("===========")
            for i, result in enumerate(test_result, 1):
                self.stdout.write(f"Result {i}:")
                self.stdout.write(result[:100] + "..." if len(result) > 100 else result)
            self.stdout.write(self.style.SUCCESS("\n✓ RAG system is working correctly!"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠ RAG system returned no results."))
        
        self.stdout.write(self.style.SUCCESS("\n✓ RAG activation complete!"))
        self.stdout.write("\nTest it by sending a query to the API:")
        self.stdout.write('curl -X POST "http://localhost:8000/api/chat/" -H "Content-Type: application/json" -d \'{"message": "What are natural predators for aphids?"}\'')
        self.stdout.write("\nOr try it through the web interface.") 