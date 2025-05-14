# FarmLore Modelfiles Integration

## Overview

This document provides an overview of the Ollama Modelfiles integration into the FarmLore chatbot system. The integration enhances the system's efficiency and performance by using specialized models for different types of agricultural queries.

## Specialized Models

We've created the following specialized models using Ollama Modelfiles:

1. **pest_identification.modelfile**: Configured for pest identification queries
2. **pest_management.modelfile**: Configured for pest management queries
3. **indigenous_knowledge.modelfile**: Configured for queries related to indigenous agricultural practices
4. **crop_pests.modelfile**: Configured for queries about pests affecting specific crops
5. **general_query.modelfile**: Configured for general agricultural inquiries

## Model Mappings

The specialized models are mapped to query types in the `OllamaHandler` class:

```python
self.specialized_models = {
    'pest_identification': 'farmlore-pest-id',
    'pest_management': 'farmlore-pest-mgmt',
    'indigenous_knowledge': 'farmlore-indigenous',
    'crop_pests': 'farmlore-crop-pests',
    'general_query': 'farmlore-general'
}
```

## Docker Integration for Modelfiles

The custom modelfiles (e.g., `pest_identification.modelfile`, `pest_management.modelfile`, etc.) are located in the `pest-management-chatbot/farmlore-project/api/inference_engine/modelfiles/` directory.

The `ollama` service, defined in the root `docker-compose.yml` file, is configured to build a custom Docker image. The build process for this image copies these modelfiles into the `/root/.ollama/modelfiles` directory within the Ollama container. 

When the `ollama` service starts, it automatically discovers these modelfiles and creates the corresponding specialized models (e.g., `farmlore-pest-id`, `farmlore-pest-mgmt`). This means the models are built as part of the Docker image creation and service startup, managed by `docker-compose up --build`.

The `OllamaHandler` class then checks for the existence of these models within the running Ollama service rather than attempting to create them from scratch via API calls during runtime if they are missing.

## Implementation Details

### OllamaHandler Class

The `OllamaHandler` class has been updated to:

1. Initialize and manage specialized models
2. Create models from Modelfiles if they don't exist
3. Generate responses using the appropriate model based on query type

### HybridEngine Class

The `HybridEngine` class has been updated to:

1. Use specialized models for different query types
2. Route queries to the appropriate model based on query type
3. Process responses from specialized models

## Usage

When processing a query, the system:

1. Determines the query type
2. Formats the prompt using the appropriate template
3. Selects the specialized model based on the query type
4. Generates a response using the specialized model
5. Returns the response to the user

## Benefits

Using specialized models provides several benefits:

1. **Improved Response Quality**: Each model is fine-tuned for a specific type of query
2. **Reduced Hallucinations**: Models have specific system instructions to reduce hallucinations
3. **Faster Response Times**: Specialized models can be smaller and more efficient
4. **Easier Customization**: Modelfiles make it easy to update model behavior without changing code

## Next Steps

1. **Testing**: Implement unit tests to ensure that the new Modelfiles and specialized models are functioning correctly
2. **Deployment**: Deploy the updated FarmLore system to a staging environment for further testing and validation
3. **Monitoring**: Set up monitoring for the performance of the specialized models to assess their effectiveness compared to the previous implementation
