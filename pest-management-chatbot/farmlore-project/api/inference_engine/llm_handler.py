"""LLM Handler for interfacing with Ollama."""
import json
import requests
from typing import Dict, List, Optional, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaHandler:
    """Handler for Ollama LLM interactions."""
    
    def __init__(self, model: str = "tinyllama", base_url: str = "http://localhost:11434"):
        """Initialize the Ollama handler.
        
        Args:
            model: The model to use (default: "tinyllama")
            base_url: Base URL for Ollama API (default: "http://localhost:11434")
        """
        self.model = model
        self.base_url = base_url
        self.context = None  # For maintaining conversation context
        
    def _make_request(self, endpoint: str, payload: Dict) -> Dict:
        """Make a request to the Ollama API.
        
        Args:
            endpoint: API endpoint (e.g., "generate", "chat")
            payload: Request payload
            
        Returns:
            Dict: API response
        """
        url = f"{self.base_url}/api/{endpoint}"
        try:
            # Ensure the payload matches Ollama's expected format
            if endpoint == "generate":
                # Remove system from payload as it's not supported in generate
                if "system" in payload:
                    system_prompt = payload.pop("system")
                    # Prepend system prompt to the actual prompt
                    payload["prompt"] = f"{system_prompt}\n\n{payload['prompt']}"
                
                # Remove unsupported options
                if "options" in payload:
                    if "num_predict" in payload["options"]:
                        payload["options"]["num_tokens"] = payload["options"].pop("num_predict")
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Handle streaming response
            content = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            content += chunk["response"]
                    except json.JSONDecodeError:
                        continue
            
            return {"response": content}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Ollama: {str(e)}")
            raise

    async def generate_response(self, 
                              prompt: str, 
                              system_prompt: Optional[str] = None,
                              temperature: float = 0.7,
                              max_tokens: int = 500) -> str:
        """Generate a response using the Ollama model.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to guide the model's behavior
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            str: Generated response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
            }
        }
        
        if system_prompt:
            payload["prompt"] = f"{system_prompt}\n\n{prompt}"
        
        try:
            response = self._make_request("generate", payload)
            return response.get("response", "")
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble generating a response right now."

    async def enhance_prolog_response(self, 
                                    prolog_result: Union[List, Dict], 
                                    user_query: str,
                                    crop_name: Optional[str] = None) -> str:
        """Enhance Prolog's logical response with natural language.
        
        Args:
            prolog_result: Results from Prolog inference
            user_query: Original user query
            crop_name: Optional crop name for context
            
        Returns:
            str: Enhanced natural language response
        """
        # Convert any Prolog Atom objects to strings
        def convert_prolog_atoms(obj):
            if isinstance(obj, list):
                return [convert_prolog_atoms(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: convert_prolog_atoms(v) for k, v in obj.items()}
            else:
                return str(obj)
        
        try:
            # Convert Prolog result to JSON-serializable format
            prolog_data = convert_prolog_atoms(prolog_result)
            
            system_prompt = """You are a pest management expert assistant. Your role is to:
            1. Take technical pest management information
            2. Convert it into clear, helpful advice
            3. Use a friendly, professional tone
            4. Include practical, actionable steps
            5. Maintain scientific accuracy while being accessible
            """
            
            # Format the Prolog results for the LLM
            context = f"Query about: {crop_name}\n" if crop_name else ""
            context += f"User asked: {user_query}\n"
            context += f"Technical data: {json.dumps(prolog_data, indent=2)}"
            
            prompt = f"""Based on this pest management query and data:
            {context}
            
            Please provide a helpful response that:
            1. Directly answers the user's question
            2. Explains any technical terms
            3. Provides practical advice
            4. Suggests preventive measures when relevant
            5. Uses bullet points for clarity when listing multiple items
            """
            
            response = await self.generate_response(prompt, system_prompt=system_prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error enhancing Prolog response: {str(e)}")
            return "I apologize, but I encountered an error while processing the pest management information. Please try again with your query."

    async def get_pest_analysis(self, 
                              symptoms: List[str], 
                              crop: str,
                              prolog_matches: List[str]) -> str:
        """Generate detailed pest analysis based on symptoms and Prolog matches.
        
        Args:
            symptoms: List of observed symptoms
            crop: The affected crop
            prolog_matches: Potential pest matches from Prolog
            
        Returns:
            str: Detailed analysis and recommendations
        """
        system_prompt = """You are a pest identification expert. Analyze the symptoms
        and potential pest matches to provide accurate identification and advice."""
        
        prompt = f"""Given these details about a potential pest problem:
        - Crop: {crop}
        - Observed symptoms: {', '.join(symptoms)}
        - Potential pests identified: {', '.join(prolog_matches)}
        
        Please provide:
        1. Most likely pest(s) and confidence level
        2. Why these pests match the symptoms
        3. Additional symptoms to look for
        4. Immediate control measures
        5. Long-term prevention strategies
        """
        
        return await self.generate_response(
            prompt,
            system_prompt=system_prompt,
            temperature=0.3  # Lower temperature for more focused response
        )

    async def generate_prevention_tips(self, 
                                     pest: str, 
                                     crop: str,
                                     existing_methods: List[str]) -> str:
        """Generate comprehensive prevention tips for specific pest and crop.
        
        Args:
            pest: The pest to prevent
            crop: The crop to protect
            existing_methods: Known prevention methods from Prolog
            
        Returns:
            str: Detailed prevention advice
        """
        system_prompt = """You are a pest prevention specialist. Provide practical,
        environmentally-friendly prevention strategies."""
        
        prompt = f"""For {pest} affecting {crop}, and knowing these existing methods:
        {', '.join(existing_methods)}
        
        Please provide comprehensive prevention advice including:
        1. Cultural control methods
        2. Physical barriers and traps
        3. Biological control options
        4. Companion planting suggestions
        5. Monitoring and early detection tips
        """
        
        return await self.generate_response(
            prompt,
            system_prompt=system_prompt,
            temperature=0.4
        )
