from api.inference_engine.ollama_handler import OllamaHandler
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Create handler instance
handler = OllamaHandler(base_url='http://ollama:11434')

# Ensure we're trying to use the real LLM
handler.is_available = True

# Function to detect if a response looks like it came from the fallback system
def is_likely_fallback(response):
    # These phrases appear in fallback responses
    fallback_phrases = [
        "I'm unable to provide specific information at the moment",
        "consult with a local agricultural expert",
        "consider reviewing common organic practices",
        "While I'm currently operating with limited capabilities",
        "consulting traditional farming knowledge"
    ]
    
    for phrase in fallback_phrases:
        if phrase in response:
            return True
    
    return False

logger.info('===== TESTING REAL OLLAMA RESPONSES =====')
logger.info(f'Ollama is_available set to: {handler.is_available}')
logger.info(f'Actual availability from connectivity check: {handler._check_availability()}')

# Test responses with specific knowledge-requiring questions
test_prompts = [
    ("SPECIFIC_PEST", "What are the biological characteristics of tomato hornworms?"),
    ("SPECIFIC_TREATMENT", "Explain how neem oil works to control aphids at the cellular level."),
    ("TECHNICAL_QUERY", "What is the difference between pyrethrin and pyrethroid insecticides?"),
    ("INDIGENOUS_KNOWLEDGE", "What traditional pest control methods were used by indigenous farmers in Mexico?")
]

results = []

for prompt_type, prompt in test_prompts:
    logger.info(f"\n=== Testing {prompt_type} PROMPT ===")
    logger.info(f"PROMPT: {prompt}")
    response = handler.generate_response(prompt)
    logger.info(f"RESPONSE: {response}")
    
    # Determine if this looks like a fallback response
    if is_likely_fallback(response):
        logger.info("ANALYSIS: This appears to be a FALLBACK response")
        results.append(False)
    else:
        # Check for signs of a real informative response
        length_check = len(response) > 100  # Real responses tend to be longer
        detail_check = bool(re.search(r'specific|scientific|process|method|approach|technique', response.lower()))
        informative = length_check and detail_check
        
        logger.info(f"ANALYSIS: This appears to be a {'REAL LLM' if informative else 'GENERIC'} response")
        results.append(informative)

# Determine overall result
success_rate = sum(results) / len(results) if results else 0
logger.info("\n===== TEST RESULTS =====")
logger.info(f"Real responses detected: {sum(results)}/{len(results)} ({success_rate*100:.0f}%)")
if success_rate > 0.75:
    logger.info("OVERALL: Ollama LLM is working correctly and providing real knowledge-based responses")
elif success_rate > 0:
    logger.info("OVERALL: Ollama LLM is partially working, but some responses may be fallbacks or generic")
else:
    logger.info("OVERALL: Test failed - all responses appear to be fallbacks or generic responses")
    logger.info("Check Ollama service and model availability") 