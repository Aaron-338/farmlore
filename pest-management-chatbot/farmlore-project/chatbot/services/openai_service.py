import json
import openai
from django.conf import settings

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def get_chat_response(messages, tools=None):
    """Get response from OpenAI API"""
    try:
        # Prepare the API call
        kwargs = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        
        # Add tools if provided
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        # Call the API
        response = openai.chat.completions.create(**kwargs)
        
        return {
            "success": True,
            "response": response,
            "message": response.choices[0].message
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_tools_for_openai():
    """Create tools for OpenAI API"""
    return [
        {
            "type": "function",
            "function": {
                "name": "identify_pest",
                "description": "Identify a pest based on crop and symptoms",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crop": {
                            "type": "string",
                            "description": "The crop affected by the pest"
                        },
                        "early_symptoms": {
                            "type": "string",
                            "description": "Early symptoms observed on the plant"
                        },
                        "advanced_symptoms": {
                            "type": "string",
                            "description": "Advanced symptoms, if any"
                        }
                    },
                    "required": ["crop", "early_symptoms"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_pests",
                "description": "Search for pests by name or symptoms",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_control_methods",
                "description": "Get control methods for a specific pest",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pest_id": {
                            "type": "string",
                            "description": "The ID of the pest"
                        }
                    },
                    "required": ["pest_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_soil_treatments",
                "description": "Get soil treatments for a specific soil type or crop",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "soil_type": {
                            "type": "string",
                            "description": "The soil type"
                        },
                        "crop": {
                            "type": "string",
                            "description": "The crop"
                        }
                    }
                }
            }
        }
    ]