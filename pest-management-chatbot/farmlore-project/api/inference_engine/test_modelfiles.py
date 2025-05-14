"""
Test script to verify the Modelfiles integration in the FarmLore system.
This script tests:
1. The existence of Modelfiles
2. The OllamaHandler's ability to create and use specialized models
3. The HybridEngine's routing of queries to the appropriate specialized models
"""
import os
import sys
import logging
import json
import unittest
from unittest.mock import patch, MagicMock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

# Import necessary modules
from api.inference_engine.ollama_handler import OllamaHandler, MODELFILES_DIR
from api.inference_engine.prompt_templates import PromptType, format_prompt

class TestModelfilesIntegration(unittest.TestCase):
    """Test the Modelfiles integration in the FarmLore system."""

    def setUp(self):
        """Set up the test environment."""
        # Mock the requests module to avoid actual API calls
        self.requests_patch = patch('api.inference_engine.ollama_handler.requests')
        self.mock_requests = self.requests_patch.start()
        
        # Mock the Session object
        self.mock_session = MagicMock()
        self.mock_requests.Session.return_value = self.mock_session
        
        # Mock successful responses for API calls
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {"response": "Test response"}
        self.mock_session.post.return_value = self.mock_response
        self.mock_session.get.return_value = self.mock_response
        
        # Initialize the OllamaHandler with mocked requests
        self.handler = OllamaHandler(base_url="http://localhost:11434")
        self.handler.is_available = True  # Force availability for testing
        
        # Record the original specialized_models mapping for verification
        self.original_specialized_models = self.handler.specialized_models.copy()
        
    def tearDown(self):
        """Clean up after tests."""
        self.requests_patch.stop()
    
    def test_modelfiles_exist(self):
        """Test that all required Modelfiles exist."""
        expected_modelfiles = [
            'pest_identification.modelfile',
            'pest_management.modelfile',
            'indigenous_knowledge.modelfile',
            'crop_pests.modelfile',
            'general_query.modelfile'
        ]
        
        for modelfile in expected_modelfiles:
            modelfile_path = os.path.join(MODELFILES_DIR, modelfile)
            self.assertTrue(os.path.exists(modelfile_path), f"Modelfile {modelfile} does not exist")
            
            # Check that the file has content
            with open(modelfile_path, 'r') as f:
                content = f.read()
                self.assertTrue(len(content) > 0, f"Modelfile {modelfile} is empty")
                self.assertIn("FROM", content, f"Modelfile {modelfile} does not contain a FROM directive")
                self.assertIn("SYSTEM", content, f"Modelfile {modelfile} does not contain a SYSTEM directive")
    
    def test_specialized_model_mappings(self):
        """Test that the specialized model mappings are correctly defined."""
        expected_mappings = {
            'pest_identification': 'farmlore-pest-id',
            'pest_management': 'farmlore-pest-mgmt',
            'indigenous_knowledge': 'farmlore-indigenous',
            'crop_pests': 'farmlore-crop-pests',
            'general_query': 'farmlore-general'
        }
        
        for query_type, model_name in expected_mappings.items():
            self.assertIn(query_type, self.handler.specialized_models, f"Query type {query_type} not in specialized_models")
            self.assertEqual(self.handler.specialized_models[query_type], model_name, 
                            f"Expected model {model_name} for query type {query_type}, got {self.handler.specialized_models[query_type]}")
    
    def test_modelfile_paths(self):
        """Test that the modelfile paths are correctly defined."""
        expected_paths = {
            'farmlore-pest-id': os.path.join(MODELFILES_DIR, 'pest_identification.modelfile'),
            'farmlore-pest-mgmt': os.path.join(MODELFILES_DIR, 'pest_management.modelfile'),
            'farmlore-indigenous': os.path.join(MODELFILES_DIR, 'indigenous_knowledge.modelfile'),
            'farmlore-crop-pests': os.path.join(MODELFILES_DIR, 'crop_pests.modelfile'),
            'farmlore-general': os.path.join(MODELFILES_DIR, 'general_query.modelfile')
        }
        
        for model_name, path in expected_paths.items():
            self.assertIn(model_name, self.handler.modelfile_paths, f"Model {model_name} not in modelfile_paths")
            self.assertEqual(self.handler.modelfile_paths[model_name], path, 
                            f"Expected path {path} for model {model_name}, got {self.handler.modelfile_paths[model_name]}")
    
    def test_generate_response_with_specialized_model(self):
        """Test that generate_response_with_specialized_model uses the correct model."""
        # Test each query type
        for query_type, model_name in self.original_specialized_models.items():
            # Call the method with the query type
            self.handler.generate_response_with_specialized_model("Test prompt", query_type)
            
            # Check that the correct model was used
            # The last call to generate_response should have used the specialized model
            args, kwargs = self.handler.generate_response.call_args
            self.assertEqual(kwargs['model'], model_name, 
                            f"Expected model {model_name} for query type {query_type}, got {kwargs['model']}")
    
    def test_initialize_specialized_models(self):
        """Test that _initialize_specialized_models creates models if they don't exist."""
        # Mock the _get_available_models method to return an empty list
        with patch.object(self.handler, '_get_available_models', return_value=[]):
            # Mock the _create_model_from_file method
            with patch.object(self.handler, '_create_model_from_file') as mock_create:
                # Call the method
                self.handler._initialize_specialized_models()
                
                # Check that _create_model_from_file was called for each model
                self.assertEqual(mock_create.call_count, len(self.handler.modelfile_paths),
                                f"Expected {len(self.handler.modelfile_paths)} calls to _create_model_from_file, got {mock_create.call_count}")
                
                # Check that each model was created with the correct path
                for model_name, path in self.handler.modelfile_paths.items():
                    mock_create.assert_any_call(model_name, path)
    
    def test_prompt_formatting(self):
        """Test that prompts are correctly formatted for each query type."""
        # Test pest identification prompt
        pest_id_prompt = format_prompt(
            PromptType.PEST_IDENTIFICATION,
            query="What is this pest?",
            pest="aphid",
            crop="tomato"
        )
        self.assertIn("user_prompt", pest_id_prompt)
        self.assertIn("What is this pest?", pest_id_prompt["user_prompt"])
        
        # Test pest management prompt
        pest_mgmt_prompt = format_prompt(
            PromptType.PEST_MANAGEMENT,
            query="How do I control aphids?",
            pest="aphid",
            crop="tomato"
        )
        self.assertIn("user_prompt", pest_mgmt_prompt)
        self.assertIn("How do I control aphids?", pest_mgmt_prompt["user_prompt"])
        
        # Test indigenous knowledge prompt
        indigenous_prompt = format_prompt(
            PromptType.INDIGENOUS_KNOWLEDGE,
            query="Tell me about ash sprinkle method",
            practice_name="ash sprinkle",
            purpose="pest control"
        )
        self.assertIn("user_prompt", indigenous_prompt)
        self.assertIn("Tell me about ash sprinkle method", indigenous_prompt["user_prompt"])
        
        # Test general query prompt
        general_prompt = format_prompt(
            PromptType.GENERAL,
            query="Tell me about farming"
        )
        self.assertIn("user_prompt", general_prompt)
        self.assertIn("Tell me about farming", general_prompt["user_prompt"])

def run_tests():
    """Run the tests."""
    logger.info("Running Modelfiles integration tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    run_tests()
