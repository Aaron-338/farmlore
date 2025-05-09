from api.inference_engine.ollama_handler import OllamaHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Create handler instance
handler = OllamaHandler(base_url='http://ollama:11434')

# Force fallback mode
handler.is_available = False
logger.info('===== TESTING OLLAMA FALLBACK RESPONSES =====')

# Test responses
test_prompts = [
    ("QUESTION", "What are common garden pests in tomatoes?"),
    ("ADVICE", "Please suggest some methods to control aphids."),
    ("STATEMENT", "My plants have small holes in the leaves.")
]

for prompt_type, prompt in test_prompts:
    logger.info(f"\n=== Testing {prompt_type} PROMPT ===")
    logger.info(f"PROMPT: {prompt}")
    response = handler.generate_response(prompt)
    logger.info(f"RESPONSE: {response}")

logger.info("\n===== TEST COMPLETED =====")
logger.info("Remember to reset is_available=True when done testing") 