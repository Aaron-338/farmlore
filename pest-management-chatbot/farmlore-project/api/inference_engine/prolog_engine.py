"""
A mock Prolog engine since SWI-Prolog is causing issues in the Docker environment
"""
import os
import logging
import json
from .ollama_handler import OllamaHandler
from ..prolog_integration.service import PrologService

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
        
        self.prolog_service = None

        if self.use_ollama:
            logging.info(f"Initializing with Ollama integration at {self.ollama_url} using model {self.ollama_model}")
            self.ollama_handler = OllamaHandler(base_url=self.ollama_url)
            
            if self.ollama_handler.is_available:
                logging.info("Ollama integration is active and working.")
                # Initialize PrologService for RAG
                try:
                    self.prolog_service = PrologService()
                    logging.info("PrologService initialized for RAG.")
                except Exception as e:
                    logging.error(f"Failed to initialize PrologService: {e}")
                    self.prolog_service = None 
            else:
                logging.warning("Ollama integration is enabled but Ollama is not available. Using mock Prolog implementation without RAG.")
                self.use_ollama = False 
                self.prolog = Prolog() 
        else:
            logging.info("Using mock Prolog implementation (Ollama integration disabled)")
            self.prolog = Prolog() 
        
        self.knowledge_path = knowledge_path
        logging.info("PrologEngine initialized")
        
        if knowledge_path and os.path.exists(knowledge_path) and not (self.use_ollama and self.prolog_service):
            self.load_knowledge(knowledge_path)
    
    def load_knowledge(self, knowledge_path):
        logging.info(f"PrologEngine loading knowledge from {knowledge_path}")
        if not self.use_ollama and hasattr(self, 'prolog'):
            self.prolog.consult(knowledge_path)

    def _format_prolog_context_for_llm(self, context: dict) -> str:
        """Formats the structured context from PrologService into a readable string for the LLM."""
        if not context or context.get('generic_response'):
            return "No specific information found in the local knowledge base."

        parts = []

        def format_dict_nicely(d, indent=0):
            """Helper to format a dictionary into readable lines."""
            dict_parts = []
            for key, value in d.items():
                key_str = key.replace("_", " ").capitalize()
                if isinstance(value, list):
                    list_str = ", ".join(map(str, value)) if value else "N/A"
                    dict_parts.append(f"{'  ' * indent}{key_str}: {list_str}")
                elif isinstance(value, dict):
                    dict_parts.append(f"{'  ' * indent}{key_str}:")
                    dict_parts.extend(format_dict_nicely(value, indent + 1))
                else:
                    dict_parts.append(f"{'  ' * indent}{key_str}: {value if value else 'N/A'}")
            return dict_parts

        if 'pest_found' in context:
            parts.append(f"Pest: {context['pest_found']}")
            if 'pest_info' in context.get('pest_info', {}):
                parts.append("Information:")
                parts.extend(format_dict_nicely(context['pest_info'], indent=1))
            
            if context.get('solutions'):
                parts.append("Solutions:")
                for sol in context['solutions']:
                    if isinstance(sol, dict):
                        sol_name = sol.get('name', 'Unnamed Solution').replace("_", " ").capitalize()
                        parts.append(f"  - {sol_name}:")
                        details_to_print = {k: v for k, v in sol.items() if k != 'name'}
                        if details_to_print:
                            parts.extend(format_dict_nicely(details_to_print, indent=2))
                        elif not details_to_print and not sol_name == 'Unnamed Solution':
                             parts.append(f"    (No further details provided in KB for {sol_name})")
                    else:
                        parts.append(f"  - {sol}")
            
            if context.get('recommendation'):
                parts.append("Recommendation:")
                if isinstance(context['recommendation'], dict):
                    rec_name = context['recommendation'].get('name', 'Unnamed Recommendation').replace("_", " ").capitalize()
                    parts.append(f"  - {rec_name}:")
                    details_to_print = {k: v for k, v in context['recommendation'].items() if k != 'name'}
                    if details_to_print:
                        parts.extend(format_dict_nicely(details_to_print, indent=2))
                    elif not details_to_print and not rec_name == 'Unnamed Recommendation':
                        parts.append(f"    (No further details provided in KB for {rec_name})")
                else:
                     parts.append(f"  - {context['recommendation']}")

        elif 'practice_found' in context:
            parts.append(f"Practice: {context['practice_found']}")
            if 'practice_info' in context.get('practice_info', {}):
                parts.append("Information:")
                parts.extend(format_dict_nicely(context['practice_info'], indent=1))
        
        if not parts:
             return "No specific information found in the local knowledge base matching the query structure."

        return "\n".join(parts)

    def query(self, query_str):
        logging.info(f"PrologEngine querying: {query_str}")
        
        if self.use_ollama and self.ollama_handler and self.ollama_handler.is_available:
            prolog_context_str = "No specific information found in the knowledge base."
            if self.prolog_service:
                try:
                    logging.info(f"Attempting to retrieve context from PrologService for query: {query_str}")
                    retrieved_context = self.prolog_service.search_prolog_kb(query_str)
                    
                    prolog_context_str = self._format_prolog_context_for_llm(retrieved_context)
                    
                    if prolog_context_str != "No specific information found in the local knowledge base." and \ 
                       prolog_context_str != "No specific information found in the local knowledge base matching the query structure." and \ 
                       "Error retrieving" not in prolog_context_str : 
                        logging.info(f"Formatted context from Prolog:\n{prolog_context_str}")
                    else:
                        logging.info("No specific context found or formatted by _format_prolog_context_for_llm.")

                except Exception as e:
                    logging.error(f"Error querying PrologService or formatting context: {e}")
                    prolog_context_str = "Error retrieving or formatting information from the knowledge base."

            prompt = f"""
You are a helpful agricultural assistant for the FarmLore system.
Your knowledge base contains information on pests, crops, and sustainable farming practices.

When answering the user's query, first consider the following information retrieved from our local Prolog knowledge base:
--- Knowledge Base Context ---
{prolog_context_str}
--- End of Knowledge Base Context ---

User Query: "{query_str}"

Please synthesize an answer based on both the Knowledge Base Context (if relevant and not an error message) and your general knowledge.
If the Knowledge Base Context directly answers the query, prioritize it.
If the context is partial or not directly relevant, supplement with your general knowledge.
If the context indicates an error or no information, state that the local knowledge base didn't have specific details and answer based on general knowledge.
Provide a comprehensive and helpful answer.
"""
            logging.debug(f"Generated prompt for Ollama:\n{prompt}")
            response = self.ollama_handler.generate_response(prompt, model=self.ollama_model)
            return [{"response": response, "source": "LLM_with_RAG_context" if prolog_context_str != "No specific information found in the knowledge base." and "Error retrieving" not in prolog_context_str else "LLM_no_RAG_context"}]
        elif hasattr(self, 'prolog'): 
            logging.info("Using mock Prolog for query.")
            results = list(self.prolog.query(query_str))
            return [{"response": results, "source": "MockProlog"}]
        else:
            logging.error("PrologEngine not configured to handle query. Neither Ollama nor MockProlog is active.")
            return [{"response": "Engine not configured.", "source": "Error"}]
    
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
