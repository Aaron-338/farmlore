from api.inference_engine.ollama_handler import OllamaHandler

# Create handler instance
handler = OllamaHandler(base_url='http://ollama:11434')

# Set is_available to True to revert any previous testing
handler.is_available = True
print('Ollama handler reset: is_available is now set to True')
print(f'Actual availability based on connectivity check: {handler._check_availability()}')
print('\nNOTE: The handler should now use the actual Ollama service when available,')
print('rather than the fallback responses used during testing.') 