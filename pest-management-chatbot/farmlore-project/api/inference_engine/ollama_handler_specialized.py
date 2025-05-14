"""
Method to add to the OllamaHandler class for generating responses with specialized models.
This file contains the method that needs to be manually added to the ollama_handler.py file.
"""

@record_llm_performance
def generate_response_with_specialized_model(self, prompt, query_type):
    """
    Generate a response using the appropriate specialized model for the query type
    
    Args:
        prompt: The prompt to send to the model
        query_type: The type of query (pest_identification, pest_management, etc.)
        
    Returns:
        The generated response text or None if an error occurred
    """
    # Select the appropriate model based on query type
    model = self.specialized_models.get(query_type, self.ollama_model)
    
    logger.info(f"Using specialized model '{model}' for query type: {query_type}")
    
    # Generate response using the selected model
    return self.generate_response(prompt=prompt, model=model)
