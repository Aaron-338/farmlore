"""
Prompt templates for Ollama LLM interactions.

This module provides a system for creating and managing prompt templates
for different types of interactions with the Ollama LLM.
"""

import logging
from typing import Dict, List, Any, Optional
from enum import Enum
from .custom_prompts import CUSTOM_PROMPTS

logger = logging.getLogger(__name__)

class PromptType(Enum):
    """Types of prompts that can be used with the LLM."""
    
    GENERAL = "general"
    PEST_IDENTIFICATION = "pest_identification"
    PEST_MANAGEMENT = "pest_management"
    SOIL_ANALYSIS = "soil_analysis"
    CROP_RECOMMENDATION = "crop_recommendation"
    KNOWLEDGE_VALIDATION = "knowledge_validation"
    FARMING_PRACTICE = "farming_practice"
    INDIGENOUS_KNOWLEDGE = "indigenous_knowledge"

class PromptTemplate:
    """
    A template for generating prompts for the LLM.
    
    This class encapsulates the structure and formatting of prompts
    for different types of queries, ensuring consistent and optimized
    interactions with the LLM.
    """
    
    def __init__(
        self,
        prompt_type: PromptType,
        system_prompt: str,
        user_template: str,
        variables: List[str] = None,
        version: str = "1.0",
        description: str = "",
    ):
        """
        Initialize a prompt template.
        
        Args:
            prompt_type: The type of prompt
            system_prompt: The system prompt that guides the LLM's behavior
            user_template: The template for the user's message with {variable} placeholders
            variables: List of variable names expected in the template
            version: Version of the template
            description: Description of what this template is used for
        """
        self.prompt_type = prompt_type
        self.system_prompt = system_prompt
        self.user_template = user_template
        self.variables = variables or []
        self.version = version
        self.description = description
    
    def format(self, **kwargs) -> Dict[str, str]:
        """
        Format the prompt with the provided variables.
        
        Args:
            **kwargs: Key-value pairs for variables in the template
            
        Returns:
            Dict containing system_prompt and user_prompt
        """
        # Validate that all required variables are provided
        missing_vars = [var for var in self.variables if var not in kwargs]
        if missing_vars:
            logger.warning(f"Missing variables in prompt: {', '.join(missing_vars)}")
            # If query is available, use simplified template
            if 'query' in kwargs:
                logger.info("Using simplified template with query only")
                return {
                    "system_prompt": self.system_prompt,
                    "user_prompt": kwargs['query']
                }
            # Fill missing variables with placeholders to avoid KeyError
            for var in missing_vars:
                kwargs[var] = f"[{var}]"
        
        # Format the user prompt with the provided variables
        try:
            user_prompt = self.user_template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Error formatting prompt template: {str(e)}")
            # Fallback to a simpler prompt if formatting fails
            user_prompt = kwargs.get("query", "Please provide information.")
        
        return {
            "system_prompt": self.system_prompt,
            "user_prompt": user_prompt
        }

# Dictionary of available templates
TEMPLATES: Dict[PromptType, PromptTemplate] = {
    PromptType.GENERAL: PromptTemplate(
        prompt_type=PromptType.GENERAL,
        system_prompt=CUSTOM_PROMPTS["general"]["system_prompt"],
        user_template=CUSTOM_PROMPTS["general"]["user_prompt"],
        variables=["query"],
        description="Generic prompt for general queries"
    ),
    
    PromptType.PEST_IDENTIFICATION: PromptTemplate(
        prompt_type=PromptType.PEST_IDENTIFICATION,
        system_prompt=CUSTOM_PROMPTS["pest_identification"]["system_prompt"],
        user_template=CUSTOM_PROMPTS["pest_identification"]["user_prompt"],
        variables=["query"],
        description="Template for pest identification queries"
    ),
    
    PromptType.PEST_MANAGEMENT: PromptTemplate(
        prompt_type=PromptType.PEST_MANAGEMENT,
        system_prompt=CUSTOM_PROMPTS["pest_management"]["system_prompt"],
        user_template=CUSTOM_PROMPTS["pest_management"]["user_prompt"],
        variables=["query"],
        description="Template for pest management recommendations"
    ),
    
    PromptType.SOIL_ANALYSIS: PromptTemplate(
        prompt_type=PromptType.SOIL_ANALYSIS,
        system_prompt="""You are a soil health specialist helping farmers in Lesotho.
Focus on practical soil assessment and improvement techniques accessible to small-scale farmers.
Emphasize sustainable soil management practices that build long-term soil health.
Balance traditional knowledge with scientific understanding of soil properties.""",
        user_template="""I need advice on my soil with these characteristics:

Soil appearance: {soil_description}
Location: {location}
Current crops: {current_crops}
Problems observed: {problems}

How can I assess and improve this soil using local resources?""",
        variables=["soil_description", "location", "current_crops", "problems"],
        description="Template for soil analysis and improvement advice"
    ),
    
    PromptType.INDIGENOUS_KNOWLEDGE: PromptTemplate(
        prompt_type=PromptType.INDIGENOUS_KNOWLEDGE,
        system_prompt="""You are an indigenous knowledge specialist for Lesotho agriculture.
Your role is to respectfully explain traditional farming practices and their ecological significance.
Emphasize the value of indigenous knowledge while acknowledging its complementary relationship with modern approaches.
Present information in a way that honors cultural heritage while examining practical applications.""",
        user_template="""I'm interested in learning about the traditional practice of {practice_name} in Lesotho farming.

What can you tell me about:
- How this practice is traditionally performed
- The ecological principles behind it
- Its effectiveness for {purpose}
- How it's being preserved or adapted today""",
        variables=["practice_name", "purpose"],
        description="Template for inquiries about indigenous knowledge and practices"
    ),
}

def get_template(prompt_type: PromptType) -> PromptTemplate:
    """
    Get a prompt template by type.
    
    Args:
        prompt_type: The type of prompt template to retrieve
        
    Returns:
        The requested prompt template or the general template if not found
    """
    return TEMPLATES.get(prompt_type, TEMPLATES[PromptType.GENERAL])

def format_prompt(prompt_type: PromptType, **kwargs) -> Dict[str, str]:
    """
    Format a prompt using the specified template.
    
    Args:
        prompt_type: The type of prompt to format
        **kwargs: Variables to insert into the template
        
    Returns:
        Dict containing system_prompt and user_prompt
    """
    template = get_template(prompt_type)
    return template.format(**kwargs)

def detect_prompt_type(query: str) -> PromptType:
    """
    Detect the appropriate prompt type based on query content.
    
    Args:
        query: The user's query
        
    Returns:
        The detected prompt type
    """
    query_lower = query.lower()
    
    # Pest identification keywords
    if any(term in query_lower for term in ["identify", "what pest", "what insect", "what disease"]):
        return PromptType.PEST_IDENTIFICATION
    
    # Pest management keywords
    if any(term in query_lower for term in ["control", "manage", "get rid of", "treat", "pesticide"]):
        return PromptType.PEST_MANAGEMENT
    
    # Soil analysis keywords
    if any(term in query_lower for term in ["soil", "fertility", "nutrients", "ph", "drainage"]):
        return PromptType.SOIL_ANALYSIS
    
    # Indigenous knowledge keywords
    if any(term in query_lower for term in ["traditional", "indigenous", "ancestors", "cultural", "old methods"]):
        return PromptType.INDIGENOUS_KNOWLEDGE
    
    # Default to general if no specific type is detected
    return PromptType.GENERAL 