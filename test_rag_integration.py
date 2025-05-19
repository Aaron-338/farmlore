#!/usr/bin/env python
"""
Test script for verifying the RAG integration with HybridEngine.
This script directly tests the implementation to ensure it works correctly.
"""

import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_rag_integration")

def test_rag_converter():
    """Test the PrologToRAGConverter class directly"""
    logger.info("\n=== Testing PrologToRAGConverter ===")
    
    try:
        from implement_rag import PrologToRAGConverter
        
        # Create a temporary directory for the test
        temp_dir = Path("./temp_rag_test")
        temp_dir.mkdir(exist_ok=True)
        
        # Initialize the converter
        converter = PrologToRAGConverter(persist_directory=str(temp_dir))
        logger.info("PrologToRAGConverter initialized successfully")
        
        # Find knowledge bases
        kb_files = []
        for file in Path(".").glob("*.pl"):
            kb_files.append(str(file))
        
        if not kb_files:
            logger.error("No Prolog files found in current directory")
            return False
        
        logger.info(f"Found {len(kb_files)} Prolog files: {kb_files}")
        
        # Extract knowledge from first file
        test_file = kb_files[0]
        chunks = converter.extract_knowledge_from_prolog(test_file)
        
        if not chunks:
            logger.error(f"No text chunks extracted from {test_file}")
            return False
        
        logger.info(f"Successfully extracted {len(chunks)} text chunks from {test_file}")
        logger.info(f"Sample chunk: {chunks[0][:200]}...")
        
        # Create vector store
        vector_store = converter.create_vector_store(chunks)
        
        if not vector_store:
            logger.error("Failed to create vector store")
            return False
        
        logger.info("Vector store created successfully")
        return True
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}. Make sure RAG dependencies are installed.")
        return False
    except Exception as e:
        logger.error(f"Error testing RAG converter: {str(e)}")
        return False

def test_rag_query():
    """Test the RAG query functionality"""
    logger.info("\n=== Testing RAG Query ===")
    
    try:
        from implement_rag import PrologToRAGConverter, RAGQuery
        
        # Use the temporary directory from previous test
        temp_dir = Path("./temp_rag_test")
        
        # Check if vector store exists
        if not temp_dir.exists():
            logger.error("Vector store directory not found. Run test_rag_converter first.")
            return False
        
        # Initialize the converter and load vector store
        converter = PrologToRAGConverter(persist_directory=str(temp_dir))
        vector_store = converter.load_vector_store()
        
        if not vector_store:
            logger.error("Failed to load vector store")
            return False
        
        logger.info("Vector store loaded successfully")
        
        # Create RAG query
        rag_query = RAGQuery(vector_store)
        logger.info("RAG query initialized successfully")
        
        # Test queries
        test_queries = [
            "How do I control aphids on roses?",
            "What indigenous methods are used for controlling pests on maize?",
            "What are organic methods for pest control?"
        ]
        
        for query in test_queries:
            logger.info(f"\nTesting query: {query}")
            
            # Query the RAG system
            results = rag_query.query(query, k=2)
            
            if not results:
                logger.warning(f"No results found for query: {query}")
                continue
            
            logger.info(f"Found {len(results)} results")
            for i, result in enumerate(results):
                logger.info(f"Result {i+1}: {result[:200]}...")
        
        return True
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}. Make sure RAG dependencies are installed.")
        return False
    except Exception as e:
        logger.error(f"Error testing RAG query: {str(e)}")
        return False

def test_hybrid_engine_integration():
    """Test integration with HybridEngine"""
    logger.info("\n=== Testing HybridEngine Integration ===")
    
    try:
        # Import the necessary modules
        from implement_rag import extend_hybrid_engine
        
        # Try to import HybridEngine
        try:
            from api.inference_engine.hybrid_engine import HybridEngine
        except ImportError:
            logger.error("Could not import HybridEngine. Make sure you're running this script from the correct directory.")
            return False
        
        # Create a new HybridEngine instance
        engine = HybridEngine()
        logger.info("Created new HybridEngine instance")
        
        # Log available methods
        method_list = [m for m in dir(engine) if not m.startswith('_') and callable(getattr(engine, m))]
        logger.info(f"Available methods in HybridEngine: {method_list}")
        
        # Extend the HybridEngine with RAG capabilities
        extend_hybrid_engine(engine)
        
        # Check if RAG system is attached
        if not hasattr(engine, 'rag_system'):
            logger.error("RAG system not attached to HybridEngine")
            return False
        
        logger.info("RAG system successfully attached to HybridEngine")
        
        # Test a query if we have process_query method
        if hasattr(engine, 'process_query'):
            logger.info("Testing process_query method with RAG...")
            
            query_type = "pest_management"
            params = {"query": "How do I control aphids on roses?"}
            
            result = engine.process_query(query_type, params)
            logger.info(f"Query result source: {result.get('source', 'unknown')}")
            logger.info(f"Query result: {result.get('response', '')[:200]}...")
        
        return True
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}. Make sure all dependencies are installed.")
        return False
    except Exception as e:
        logger.error(f"Error testing HybridEngine integration: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== RAG Integration Test ===")
    
    # Test RAG converter
    converter_success = test_rag_converter()
    print(f"RAG converter test: {'SUCCESS' if converter_success else 'FAILED'}")
    
    # Test RAG query
    if converter_success:
        query_success = test_rag_query()
        print(f"RAG query test: {'SUCCESS' if query_success else 'FAILED'}")
    
    # Test HybridEngine integration
    engine_success = test_hybrid_engine_integration()
    print(f"HybridEngine integration test: {'SUCCESS' if engine_success else 'FAILED'}")
    
    # Clean up
    import shutil
    temp_dir = Path("./temp_rag_test")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print(f"Cleaned up temporary test directory: {temp_dir}")
    
    if converter_success and (not engine_success):
        print("\nRAG components work correctly, but HybridEngine integration failed.")
        print("This may be due to differences in the HybridEngine implementation.")
        print("Try running the script inside the Docker container where the actual HybridEngine is available.")
        sys.exit(1)
    elif converter_success:
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\nRAG converter test failed. Check the logs for details.")
        sys.exit(1) 