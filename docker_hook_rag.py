#!/usr/bin/env python3
"""
Script to hook the RAG system directly into the HybridEngine in Docker.
"""
import os
import sys
import logging
import json
import types

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def hook_rag_into_hybrid_engine():
    """
    Hook the RAG system directly into the HybridEngine.
    """
    try:
        # Add the app directory to the path
        sys.path.append('/app')
        
        # Set RAG environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Create the ChromaDB directory if it doesn't exist
        os.makedirs(os.environ['RAG_PERSIST_DIR'], exist_ok=True)
        
        # Import required modules
        try:
            from api.inference_engine.hybrid_engine import HybridEngine
            import api.inference_engine.hybrid_engine as hybrid_engine_module
        except ImportError:
            logger.error("Failed to import HybridEngine. Make sure you're in the correct environment.")
            return False
        
        # Get the hybrid engine instance
        engine_instance = None
        
        # Look for the engine instance in the imported module's attributes
        for attr_name in dir(hybrid_engine_module):
            attr = getattr(hybrid_engine_module, attr_name)
            if isinstance(attr, HybridEngine):
                engine_instance = attr
                logger.info(f"Found HybridEngine instance: {attr_name}")
                break
        
        if not engine_instance:
            logger.info("No existing HybridEngine instance found. Creating a new one.")
            engine_instance = HybridEngine()
        
        # Import RAG modules
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
        except ImportError:
            logger.error("Failed to import LangChain modules. Make sure they're installed.")
            return False
        
        # Create a simple RAG class for direct integration
        class SimpleRAG:
            def __init__(self, persist_dir):
                self.persist_dir = persist_dir
                self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                
                if os.path.exists(persist_dir):
                    self.vector_store = Chroma(
                        embedding_function=self.embeddings,
                        persist_directory=persist_dir
                    )
                else:
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
        
        # Create and attach the RAG system to the engine instance
        logger.info("Creating and attaching RAG system...")
        engine_instance.rag_system = SimpleRAG(os.environ['RAG_PERSIST_DIR'])
        
        # Test a query to make sure it works
        test_query = "What are natural predators for aphids?"
        rag_results = engine_instance.rag_system.query(test_query)
        
        if rag_results:
            logger.info("RAG system successfully queried!")
            print("\nRAG Results:")
            print("===========")
            for i, result in enumerate(rag_results, 1):
                print(f"Result {i}:")
                print(result)
                print("-" * 40)
        else:
            logger.warning("RAG system query returned no results.")
        
        # Create a wrapper around the query method to include RAG results
        original_query = engine_instance.query
        
        def query_with_rag(self, query_type, params=None):
            """Wrap the query method to include RAG results"""
            if params is None:
                params = {}
            
            # Extract the query from params
            user_query = params.get("query", "") or params.get("message", "")
            
            # Check if this is a query type that could benefit from RAG
            if query_type in ["general", "general_query", "pest_management", "control_methods", "pest_identification"]:
                logger.info(f"Querying RAG system for query type: {query_type}")
                rag_results = self.rag_system.query(user_query)
                
                if rag_results:
                    logger.info(f"RAG found {len(rag_results)} relevant results")
                    # Get the original result
                    original_result = original_query(query_type, params)
                    
                    # Add RAG info to the response
                    rag_content = "Based on our knowledge base:\n\n" + "\n\n".join(rag_results)
                    
                    # If the original result has a response, combine it with RAG info
                    if isinstance(original_result, dict) and "response" in original_result:
                        if "pest predators" in user_query.lower() or "natural predators" in user_query.lower() or "aphid" in user_query.lower():
                            # For predator queries, prioritize RAG results
                            original_result["response"] = rag_content + "\n\nAdditional information:\n" + original_result["response"]
                            original_result["source"] = "rag_combined"
                        else:
                            # For other queries, add RAG as additional info
                            original_result["response"] += "\n\nAdditional information from our knowledge base:\n" + rag_content
                            original_result["source"] = "hybrid_rag"
                    
                    return original_result
            
            # For non-RAG queries or if RAG found nothing, use the original method
            return original_query(query_type, params)
        
        # Replace the query method with our RAG-enhanced version
        engine_instance.query = types.MethodType(query_with_rag, engine_instance)
        
        logger.info("Successfully hooked RAG into the HybridEngine")
        print("\n✓ RAG system has been successfully hooked into the HybridEngine!")
        return True
        
    except Exception as e:
        logger.error(f"Error hooking RAG into HybridEngine: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Hooking RAG system into HybridEngine...")
    success = hook_rag_into_hybrid_engine()
    if success:
        print("\n✓ RAG system successfully integrated with HybridEngine!")
        print("\nTest it by sending a query like:")
        print('curl -X POST "http://localhost:8000/api/chat/" -H "Content-Type: application/json" -d \'{"message": "What are natural predators for aphids?"}\'')
    else:
        print("\n⚠ Failed to hook RAG into HybridEngine. See logs for details.") 