import sys

def modify_error_message(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find and replace the specific error message pattern in return statements
    modified_content = content.replace(
        'return {\n                    "error": f"HybridEngine Error: {str(e)}",\n                    "response": f"I encountered an error', 
        'return {\n                    "error": f"HybridEngine Error: {str(e)}",\n                    "response": f"TEST ERROR TEST - I encountered an error'
    )
    
    # Write back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    print(f"Modified {file_path} successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        modify_error_message(file_path)
    else:
        print("Please provide file path as argument.") 