from api.inference_engine.ollama_handler import OllamaHandler

# Create handler instance
handler = OllamaHandler(base_url='http://ollama:11434')

# Force fallback mode
handler.is_available = False
print('Testing in forced fallback mode (Ollama unavailable)')
print('-' * 70)

# Test different types of queries
question = 'What are common garden pests in tomatoes?'
print(f'QUESTION QUERY: "{question}"')
q_response = handler.generate_response(question)
print(f'RESPONSE: "{q_response}"')
print('-' * 70)

advice = 'Please suggest some methods to control aphids.'
print(f'ADVICE QUERY: "{advice}"')
a_response = handler.generate_response(advice)
print(f'RESPONSE: "{a_response}"')
print('-' * 70)

statement = 'My plants have small holes in the leaves.'
print(f'STATEMENT QUERY: "{statement}"')
s_response = handler.generate_response(statement)
print(f'RESPONSE: "{s_response}"')
print('-' * 70) 