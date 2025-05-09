"""
A mock Prolog engine since SWI-Prolog is causing issues in the Docker environment
"""
import os
import logging
from .ollama_handler import OllamaHandler

# Mock Prolog class that mimics the interface of pyswip.Prolog
class Prolog:
    def __init__(self):
        self.facts = []
        logging.info("Mock Prolog engine initialized")
    
    def consult(self, filename):
        logging.info(f"Mock Prolog engine consulting file: {filename}")
        return True
    
    def assertz(self, fact):
        self.facts.append(fact)
        logging.info(f"Mock Prolog engine asserting fact: {fact}")
        return True
    
    def query(self, query):
        logging.info(f"Mock Prolog engine querying: {query}")
        # Return a mock result
        return [{}]  # Empty result with one solution

class PrologEngine:
    def __init__(self, knowledge_path=None):
        # Check if Ollama should be used
        self.use_ollama = os.environ.get('USE_OLLAMA', 'false').lower() == 'true'
        self.ollama_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model = os.environ.get('OLLAMA_MODEL', 'gemma:2b')
        
        if self.use_ollama:
            logging.info(f"Initializing with Ollama integration at {self.ollama_url} using model {self.ollama_model}")
            self.ollama_handler = OllamaHandler(base_url=self.ollama_url)
            
            if self.ollama_handler.is_available:
                logging.info("Ollama integration is active and working")
            else:
                logging.warning("Ollama integration is enabled but Ollama is not available. Using mock implementation.")
                self.use_ollama = False
                self.prolog = Prolog()
        else:
            logging.info("Using mock Prolog implementation (Ollama integration disabled)")
            self.prolog = Prolog()
        
        self.knowledge_path = knowledge_path
        logging.info("PrologEngine initialized")
        
        if knowledge_path and os.path.exists(knowledge_path):
            self.load_knowledge(knowledge_path)
    
    def load_knowledge(self, knowledge_path):
        logging.info(f"PrologEngine loading knowledge from {knowledge_path}")
        if not self.use_ollama:
            self.prolog.consult(knowledge_path)
        # With Ollama, knowledge is processed through prompts rather than loaded from files
    
    def query(self, query_str):
        logging.info(f"PrologEngine querying: {query_str}")
        
        if self.use_ollama and self.ollama_handler.is_available:
            # Format the query as a prompt for Ollama
            prompt = f"""
            You are a pest management expert. Please answer the following query:
            {query_str}
            """
            # Get response from Ollama
            response = self.ollama_handler.generate_response(prompt, model=self.ollama_model)
            # Convert to a format similar to what Prolog would return
            return [{"response": response}]
        else:
            # Use mock Prolog
            results = list(self.prolog.query(query_str))
            return results
    
    def assert_fact(self, fact):
        logging.info(f"PrologEngine asserting fact: {fact}")
        if not self.use_ollama:
            self.prolog.assertz(fact)
        # With Ollama, facts can be included in the prompt context
    
    def consult_file(self, file_path):
        logging.info(f"PrologEngine consulting file: {file_path}")
        if not self.use_ollama:
            self.prolog.consult(file_path)
        # With Ollama, file content can be included in the prompt context
