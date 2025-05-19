# Prolog Knowledge Base RAG Implementation

This project implements a Retrieval-Augmented Generation (RAG) system for the FarmLore Prolog knowledge base, enabling natural language queries against structured pest management data.

## Overview

The RAG system converts Prolog frames (structured data) into vector embeddings that can be queried semantically. This addresses the limitation in the original system where general queries were falling back to default responses instead of leveraging the existing knowledge base.

## Components

1. **PrologToRAGConverter**: Converts Prolog frames into text chunks and creates vector embeddings
2. **RAGQuery**: Provides an interface for querying the vector database
3. **HybridEnginePatch**: Integrates the RAG system with the existing HybridEngine

## How It Works

1. Prolog frames are extracted from knowledge base files
2. Each frame is converted to a text chunk
3. Text chunks are embedded using HuggingFace's `all-MiniLM-L6-v2` model
4. Embeddings are stored in a Chroma vector database
5. User queries are embedded and matched against the knowledge base
6. Relevant chunks are retrieved and returned as responses

## Installation

```bash
# Install dependencies
pip install -r requirements_rag.txt
```

## Usage

### Standalone Testing

You can test the RAG system directly:

```python
from implement_rag import PrologToRAGConverter, RAGQuery

# Initialize and build the vector store
converter = PrologToRAGConverter()
vector_store = converter.process_all_knowledge_bases()

# Create the query system
rag = RAGQuery(vector_store)

# Query the system
results = rag.query("How do I control aphids on peas?")
for result in results:
    print(result)
```

### Integration with HybridEngine

To integrate with the existing HybridEngine:

```python
from api.inference_engine.hybrid_engine import HybridEngine
from hybrid_engine_patch import HybridEnginePatch

# Initialize the hybrid engine
engine = HybridEngine()

# Apply RAG patches
HybridEnginePatch.apply_patches(engine)

# Continue with normal initialization
```

## File Structure

- `implement_rag.py`: Core RAG implementation
- `hybrid_engine_patch.py`: Integration code for HybridEngine
- `requirements_rag.txt`: Required dependencies

## Advantages over Current Implementation

1. **Better Handling of General Queries**: Leverages existing knowledge base data instead of falling back to default responses
2. **Semantic Understanding**: Can handle queries even when they don't match exact keywords
3. **Complementary to Existing System**: Works alongside the Prolog engine rather than replacing it
4. **Lightweight**: Uses small embedding models that can run on CPU
5. **Extensible**: Can be expanded to include more knowledge sources

## Future Improvements

1. Add knowledge extraction from other sources like PDF documents
2. Implement query classification to better route between RAG and Prolog
3. Add feedback mechanisms to improve retrieval quality
4. Implement a reranking system for better result ordering
5. Create a periodic update mechanism to sync with new Prolog knowledge 