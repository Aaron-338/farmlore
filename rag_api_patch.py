#!/usr/bin/env python
"""
RAG API Patch

Simple script to patch the API views to use the standalone RAG module.
"""
import os
import re
import sys
import traceback

def patch_views_py(views_path="/app/api/views.py"):
    """Patch the views.py file to use the standalone RAG module"""
    try:
        print(f"Looking for views.py at: {views_path}")
        
        # Check if file exists
        if not os.path.exists(views_path):
            print(f"Error: views.py not found at path: {views_path}")
            return False
            
        print("Reading views.py file...")
        with open(views_path, "r") as f:
            content = f.read()
            
        # Make a backup
        backup_path = f"{views_path}.bak"
        with open(backup_path, "w") as f:
            f.write(content)
        print(f"Created backup at: {backup_path}")
        
        # Check if already patched
        if "from api.inference_engine.standalone_rag import" in content:
            print("views.py already patched with RAG module")
            return True
            
        # Add import for standalone_rag
        import_pos = content.find("import ")
        if import_pos == -1:
            print("Error: Could not find import section")
            return False
            
        # Find a newline after imports
        end_imports_pos = content.find("\n\n", import_pos)
        if end_imports_pos == -1:
            end_imports_pos = content.find("\n", import_pos)
            
        # Add our import
        rag_import = "\nfrom api.inference_engine.standalone_rag import enhance_response, rag_enhance_api_response"
        new_content = content[:end_imports_pos] + rag_import + content[end_imports_pos:]
        
        # Find the chat_view function
        chat_view_pos = new_content.find("def chat_view(request):")
        if chat_view_pos == -1:
            print("Error: Could not find chat_view function")
            return False
            
        # Find the JsonResponse
        json_response_pos = new_content.find("return JsonResponse(", chat_view_pos)
        if json_response_pos == -1:
            print("Error: Could not find JsonResponse in chat_view")
            return False
            
        # Find the last code line before the JsonResponse
        last_line_pos = new_content.rfind("\n", chat_view_pos, json_response_pos)
        if last_line_pos == -1:
            print("Error: Could not find proper position to insert RAG code")
            return False
            
        # Add RAG enhancement code
        rag_code = "\n        # Enhance response with RAG\n        try:\n            query = params.get('message', '')\n            response = rag_enhance_api_response(query, response)\n            print(f\"Enhanced response with RAG for query: {query}\")\n        except Exception as e:\n            print(f\"Error enhancing response with RAG: {str(e)}\")\n"
        
        # Insert RAG code before JsonResponse
        new_content = new_content[:last_line_pos] + rag_code + new_content[last_line_pos:]
        
        # Write updated content
        print("Writing updated views.py with RAG integration...")
        with open(views_path, "w") as f:
            f.write(new_content)
            
        print("✅ Successfully patched views.py with RAG integration")
        return True
        
    except Exception as e:
        print(f"Error patching views.py: {str(e)}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    views_path = "/app/api/views.py"
    if len(sys.argv) > 1:
        views_path = sys.argv[1]
        
    success = patch_views_py(views_path)
    
    if success:
        print("\n✅ RAG API patch completed successfully")
        sys.exit(0)
    else:
        print("\n❌ RAG API patch failed")
        sys.exit(1) 