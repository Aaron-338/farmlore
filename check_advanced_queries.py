"""
Script to check the advanced queries functionality in the Prolog knowledge base
"""
import os
import re
from pathlib import Path

def check_advanced_queries():
    """Check the advanced queries functionality in the Prolog knowledge base"""
    # Get the base directory of the project
    base_dir = Path(__file__).resolve().parent
    prolog_dir = base_dir / "pest-management-chatbot" / "farmlore-project" / "prolog_integration"
    
    print("\n===== ADVANCED QUERIES CHECK =====\n")
    
    # Check if the directory exists
    if not prolog_dir.exists():
        print(f"ERROR: Prolog integration directory not found: {prolog_dir}")
        return
    
    # Check for advanced_queries.pl
    advanced_queries_path = prolog_dir / "advanced_queries.pl"
    if not advanced_queries_path.exists():
        print(f"ERROR: advanced_queries.pl not found at {advanced_queries_path}")
        return
    
    # Read the advanced_queries.pl file
    with open(advanced_queries_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the process_query predicate
    if "process_query" in content:
        print("✓ process_query predicate found")
        
        # Extract the process_query implementation
        process_query_match = re.search(r'process_query\([^,]+,[^)]+\)\s*:-([^.]+)\.', content)
        if process_query_match:
            print("✓ process_query implementation found")
            implementation = process_query_match.group(1).strip()
            print(f"  Implementation: {implementation}")
        else:
            print("✗ process_query implementation not found")
    else:
        print("✗ process_query predicate not found")
    
    # Check for the tokenize_query predicate
    if "tokenize_query" in content:
        print("\n✓ tokenize_query predicate found")
    else:
        print("\n✗ tokenize_query predicate not found")
    
    # Check for synonym mappings
    synonym_mappings = re.findall(r'synonym_mapping\(([^,]+),\s*([^)]+)\)', content)
    if synonym_mappings:
        print(f"\n✓ Found {len(synonym_mappings)} synonym mappings")
        print("  Sample mappings:")
        for i, (term1, term2) in enumerate(synonym_mappings[:5]):
            print(f"  - {term1} -> {term2}")
        if len(synonym_mappings) > 5:
            print(f"  - ... and {len(synonym_mappings) - 5} more")
    else:
        print("\n✗ No synonym mappings found")
    
    # Check for query intent handlers
    intent_handlers = re.findall(r'identify_query_intent\(([^,]+),\s*([^)]+)\)', content)
    if intent_handlers:
        print(f"\n✓ Found {len(intent_handlers)} query intent handlers")
        print("  Intent handlers:")
        for i, (terms, intent) in enumerate(intent_handlers[:5]):
            print(f"  - {intent}")
        if len(intent_handlers) > 5:
            print(f"  - ... and {len(intent_handlers) - 5} more")
    else:
        print("\n✗ No query intent handlers found")
    
    # Check for execute_query predicates
    execute_queries = re.findall(r'execute_query\(([^,]+),\s*([^)]+)\)', content)
    if execute_queries:
        print(f"\n✓ Found {len(execute_queries)} execute_query predicates")
        print("  Execute query predicates:")
        for i, (query_type, _) in enumerate(execute_queries[:5]):
            print(f"  - {query_type}")
        if len(execute_queries) > 5:
            print(f"  - ... and {len(execute_queries) - 5} more")
    else:
        print("\n✗ No execute_query predicates found")
    
    # Check for crop rotation planning
    if "crop_rotation" in content:
        print("\n✓ Crop rotation planning functionality found")
    else:
        print("\n✗ Crop rotation planning functionality not found")
    
    # Check for seasonal pest management
    if "seasonal_pests" in content:
        print("\n✓ Seasonal pest management functionality found")
    else:
        print("\n✗ Seasonal pest management functionality not found")
    
    # Check for location-based recommendations
    if "location_based" in content or "region_specific" in content:
        print("\n✓ Location-based recommendations functionality found")
    else:
        print("\n✗ Location-based recommendations functionality not found")
    
    # Overall verification
    required_features = [
        "process_query" in content,
        "tokenize_query" in content,
        len(synonym_mappings) > 0,
        len(intent_handlers) > 0,
        len(execute_queries) > 0
    ]
    
    if all(required_features):
        print("\nVERIFICATION PASSED: Advanced queries functionality is implemented")
    else:
        print("\nVERIFICATION FAILED: Some required features are missing")
    
    print("\n===== CHECK COMPLETED =====\n")

if __name__ == "__main__":
    check_advanced_queries() 