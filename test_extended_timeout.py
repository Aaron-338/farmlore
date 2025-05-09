from api.inference_engine.ollama_handler import OllamaHandler
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

print("=== TESTING OLLAMA WITH EXTENDED TIMEOUT ===")

# Create a modified handler with much longer timeouts
handler = OllamaHandler(
    base_url="http://pest-management-chatbot-ollama-1:11434",  # Use the full container name
    timeout=120  # 2 minutes timeout
)

# Force the handler to think Ollama is available
handler.is_available = True

print(f"Created handler with timeout: {handler.timeout} seconds")
print(f"Using endpoint: {handler.api_generate}")

# Simple test with a knowledge-based query
query = "What is a tomato hornworm?"
print(f"\nTesting query: {query}")

try:
    start_time = time.time()
    response = handler.generate_response(query)
    duration = time.time() - start_time
    
    print(f"Response received in {duration:.2f} seconds")
    print(f"Response: {response}")
    
    if "I'm unable to provide specific information" in response:
        print("\nFAILED: Received fallback response, not accessing knowledge base")
    else:
        print("\nSUCCESS: Response appears to be from the knowledge base!")
        
except Exception as e:
    print(f"Error: {str(e)}")

print("\n=== TEST COMPLETED ===")
print("If you received an actual response about tomato hornworms (not a fallback message),")
print("then the system is successfully querying the knowledge base.") 