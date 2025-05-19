#!/usr/bin/env python
"""
Simple RAG Database Creator

Creates a vector database for RAG without relying on LangChain,
directly using ChromaDB and Sentence Transformers.
"""
import os
import json
import logging
import numpy as np
import traceback
from typing import List, Dict

# Configure logging - more verbose for debugging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG level for more details
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("simple_rag_db_creator")

# Sample pest management data
PEST_DATA = [
    {
        "title": "Aphid Control on Tomatoes",
        "content": """
Aphids are common pests on tomato plants. They are small, soft-bodied insects that can be green, yellow, brown, red, or black. They feed on plant sap and can cause stunted growth, yellowed leaves, and reduced yields.

Effective control methods for aphids on tomatoes include:

1. Biological control: Introduce natural predators like ladybugs, lacewings, and parasitic wasps that feed on aphids.

2. Neem oil: Apply neem oil spray, which disrupts the aphid life cycle and acts as a repellent.

3. Insecticidal soap: Use insecticidal soap sprays that are specifically designed for soft-bodied insects like aphids.

4. Water spray: Use a strong stream of water to physically remove aphids from plants.

5. Companion planting: Plant aphid-repelling plants like marigolds, nasturtiums, and garlic near tomatoes.

6. Diatomaceous earth: Apply food-grade diatomaceous earth around plants to control aphid populations.

7. Pruning: Remove heavily infested leaves and stems to prevent spread.

8. Aluminum foil mulch: Place aluminum foil around the base of plants to repel aphids with reflective light.

For severe infestations, organic or synthetic insecticides may be necessary, but always follow label instructions and consider the environmental impact.
"""
    },
    # Shorter dataset for testing
    {
        "title": "Spider Mite Management in Gardens",
        "content": """
Spider mites are tiny arachnids that can cause significant damage to garden plants. They appear as tiny moving dots, often red, brown, or yellow. Signs of infestation include fine webbing on plants and stippled, discolored leaves.

Effective management strategies include:

1. Water spray: Regular, forceful spraying with water can dislodge mites and reduce populations.

2. Increase humidity: Spider mites thrive in dry conditions, so increasing humidity can discourage them.
"""
    }
]

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks with overlap"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        if end < text_length and end < start + chunk_size:
            # Find the last period or newline to break at
            last_period = text.rfind('.', start, end)
            last_newline = text.rfind('\n', start, end)
            break_point = max(last_period, last_newline)
            
            if break_point > start:
                end = break_point + 1
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks

def create_simple_rag_database(data: List[Dict], persist_dir: str = "./data/chromadb"):
    """Create a RAG vector database using ChromaDB and Sentence Transformers directly"""
    try:
        # Print debug information about the environment
        logger.debug(f"Python path: {os.sys.path}")
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Data directory will be: {persist_dir}")
        
        # Import necessary libraries
        logger.debug("Importing chromadb and sentence_transformers")
        import chromadb
        from sentence_transformers import SentenceTransformer
        
        # Create the directory if it doesn't exist
        logger.debug(f"Creating directory: {persist_dir}")
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize sentence transformer model
        logger.debug("Initializing sentence transformer model")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Initialized sentence transformer model")
        
        # Initialize ChromaDB client
        logger.debug(f"Initializing ChromaDB client with path: {persist_dir}")
        client = chromadb.PersistentClient(path=persist_dir)
        logger.info(f"Connected to ChromaDB at {persist_dir}")
        
        # Create or get collection
        logger.debug("Creating or getting pest_management collection")
        
        # First check if collection exists and delete it (for testing purposes)
        try:
            existing_collections = client.list_collections()
            logger.debug(f"Existing collections: {existing_collections}")
            
            for collection in existing_collections:
                if collection.name == "pest_management":
                    logger.debug("Deleting existing pest_management collection")
                    client.delete_collection("pest_management")
                    break
        except Exception as e:
            logger.warning(f"Error checking/deleting existing collections: {str(e)}")
        
        # Create collection
        collection = client.create_collection(
            name="pest_management",
            metadata={"description": "Agricultural pest management information"}
        )
        logger.info("Created pest_management collection")
        
        # Prepare documents and texts
        all_chunks = []
        all_metadatas = []
        all_ids = []
        chunk_counter = 0
        
        # Process each document
        for item_idx, item in enumerate(data):
            logger.debug(f"Processing document {item_idx}: {item['title']}")
            
            # Split content into chunks
            content_chunks = chunk_text(item["content"])
            logger.debug(f"Split into {len(content_chunks)} chunks")
            
            for chunk_idx, chunk in enumerate(content_chunks):
                all_chunks.append(chunk)
                all_metadatas.append({
                    "title": item["title"],
                    "source_idx": str(item_idx),  # Convert to string for ChromaDB compatibility
                    "chunk_idx": str(chunk_idx)   # Convert to string for ChromaDB compatibility
                })
                all_ids.append(f"chunk_{chunk_counter}")
                chunk_counter += 1
        
        logger.info(f"Created {len(all_chunks)} text chunks")
        
        # Generate embeddings in batch
        logger.debug("Generating embeddings")
        embeddings = model.encode(all_chunks)
        logger.debug(f"Generated {len(embeddings)} embeddings")
        
        # Debug information about embeddings
        logger.debug(f"Embedding shape: {embeddings.shape}")
        logger.debug(f"Embedding sample: {embeddings[0][:5]}...")
        
        # Convert embeddings to lists for ChromaDB
        embeddings_list = [emb.tolist() for emb in embeddings]
        
        # Debug information about metadata and chunks
        logger.debug(f"First chunk: {all_chunks[0][:50]}...")
        logger.debug(f"First metadata: {all_metadatas[0]}")
        
        # Add documents to collection in smaller batches to avoid potential issues
        BATCH_SIZE = 10
        for i in range(0, len(all_chunks), BATCH_SIZE):
            end_idx = min(i + BATCH_SIZE, len(all_chunks))
            logger.debug(f"Adding batch {i} to {end_idx}")
            
            collection.add(
                documents=all_chunks[i:end_idx],
                metadatas=all_metadatas[i:end_idx],
                ids=all_ids[i:end_idx],
                embeddings=embeddings_list[i:end_idx]
            )
        
        logger.info(f"Added {len(all_chunks)} documents to ChromaDB collection in batches")
        
        # Save metadata about the collection for later reference
        collection_info = {
            "num_documents": len(all_chunks),
            "documents": [{"title": item["title"], "length": len(item["content"])} for item in data],
            "creation_timestamp": str(os.path.getmtime(persist_dir))
        }
        
        logger.debug(f"Writing collection info to {os.path.join(persist_dir, 'collection_info.json')}")
        with open(os.path.join(persist_dir, "collection_info.json"), "w") as f:
            json.dump(collection_info, f, indent=2)
        
        # Test a sample query
        test_query = "How do I control aphids on tomatoes?"
        logger.debug(f"Testing query: {test_query}")
        query_embedding = model.encode(test_query).tolist()
        
        logger.debug("Querying collection")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        logger.info(f"Test query: '{test_query}'")
        if results and results['documents'] and len(results['documents'][0]) > 0:
            logger.info(f"Found {len(results['documents'][0])} results")
            for i, doc in enumerate(results['documents'][0]):
                logger.info(f"Result {i+1}: {doc[:150]}...")
            return True
        else:
            logger.warning("Test query returned no results")
            return False
    
    except Exception as e:
        logger.error(f"Error creating RAG database: {str(e)}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== Simple RAG Database Creator ===")
    
    # Get persistence directory from environment or use default
    persist_dir = os.environ.get("RAG_PERSIST_DIR", "./data/chromadb")
    print(f"Creating vector database at: {persist_dir}")
    
    # Using a smaller dataset for testing
    success = create_simple_rag_database(PEST_DATA[:2], persist_dir)
    
    if success:
        print("✅ Successfully created RAG vector database!")
        print("The database now contains information on various pest management techniques.")
        print("You can now use the RAG integration to enhance query responses.")
    else:
        print("❌ Failed to create RAG vector database.")
        print("Check the logs for more information.") 