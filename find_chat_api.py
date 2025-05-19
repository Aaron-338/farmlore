#!/usr/bin/env python
"""
Find Chat API

This script locates the chat API function in the Django views.
"""
import os
import re
import sys
from pathlib import Path

def find_api_views():
    """Find all potential API view files"""
    api_dir = Path("/app/api")
    if not api_dir.exists():
        print(f"API directory not found: {api_dir}")
        return []
        
    view_files = []
    for path in api_dir.glob("**/*.py"):
        with open(path, "r") as f:
            content = f.read()
            # Check if this might be a views file
            if "JsonResponse" in content or "def " in content:
                view_files.append(path)
                
    return view_files

def find_chat_function(path):
    """Find the chat function in the given file"""
    try:
        with open(path, "r") as f:
            content = f.read()
            
        # Look for functions
        functions = []
        for match in re.finditer(r'def\s+([^\(]+)\(', content):
            func_name = match.group(1)
            functions.append(func_name)
            
        # Look for chat-related functions
        chat_functions = [f for f in functions if "chat" in f.lower()]
        
        # Look for JsonResponse near chat-related text
        chat_response_pos = content.find("JsonResponse")
        if chat_response_pos != -1:
            # Get surrounding context
            start = max(0, chat_response_pos - 200)
            end = min(len(content), chat_response_pos + 200)
            context = content[start:end]
            
            return {
                "path": str(path),
                "functions": functions,
                "chat_functions": chat_functions,
                "has_json_response": "JsonResponse" in content,
                "response_context": context
            }
        
        return {
            "path": str(path),
            "functions": functions,
            "chat_functions": chat_functions,
            "has_json_response": "JsonResponse" in content
        }
    except Exception as e:
        return {
            "path": str(path),
            "error": str(e)
        }

if __name__ == "__main__":
    print("Searching for API view files...")
    view_files = find_api_views()
    
    if not view_files:
        print("No API view files found")
        sys.exit(1)
        
    print(f"Found {len(view_files)} potential API view files:")
    for i, path in enumerate(view_files, 1):
        print(f"{i}. {path}")
        
    print("\nAnalyzing files for chat functions...")
    for path in view_files:
        result = find_chat_function(path)
        print(f"\n--- Analysis for {result['path']} ---")
        
        if "error" in result:
            print(f"Error: {result['error']}")
            continue
            
        print(f"Functions: {', '.join(result['functions'])}")
        print(f"Chat-related functions: {', '.join(result['chat_functions'])}")
        print(f"Has JsonResponse: {result['has_json_response']}")
        
        if "response_context" in result:
            print("\nJSON Response context:")
            print(result["response_context"]) 