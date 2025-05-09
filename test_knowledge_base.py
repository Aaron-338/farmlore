from api.inference_engine.ollama_handler import OllamaHandler

# Create handler instance with real Ollama endpoint
handler = OllamaHandler(base_url='http://ollama:11434')

print("\n=== KNOWLEDGE BASE VERIFICATION TEST ===")
print(f"Is Ollama available: {handler.is_available}")

# 1. Use a very specific query that would only be answered correctly with real knowledge
query = "What are the symptoms of late blight on tomato plants? Be specific."
print(f"\nQuery: {query}")

# Get response
response = handler.generate_response(query)
print(f"\nResponse:\n{response}")

# 2. Verification - let's ask a question with a specific factual answer we can verify
factual_query = "What is the scientific name of the tomato hornworm moth?"
print(f"\nFactual Query: {factual_query}")

factual_response = handler.generate_response(factual_query)
print(f"\nFactual Response:\n{factual_response}")

# Check if the scientific name (Manduca quinquemaculata) is in the response
is_factual = "manduca" in factual_response.lower() or "quinquemaculata" in factual_response.lower()
print(f"\nContains expected scientific name: {is_factual}")

if is_factual:
    print("\nVERIFICATION PASSED: The system is querying a real knowledge base")
else:
    print("\nVERIFICATION FAILED: The system may be using mock responses or has limited knowledge")
    
print("\nNote: If you see detailed information about late blight symptoms (dark lesions, leaf spots, etc.)")
print("and the correct scientific name, this confirms the system is using its knowledge base.") 