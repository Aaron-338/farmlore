"""
Test script for the local Prolog knowledge base
This script tests the Prolog knowledge base directly by inspecting the files
"""
import os
import sys
import logging
import re
from pathlib import Path

# Configure logging with a more visible format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_prolog_knowledge_base():
    """Test the Prolog knowledge base by inspecting files"""
    # Get the base directory of the project
    base_dir = Path(__file__).resolve().parent
    prolog_dir = base_dir / "pest-management-chatbot" / "farmlore-project" / "prolog_integration"
    
    print("\n===== PROLOG KNOWLEDGE BASE TEST =====\n")
    print(f"Looking for Prolog files in: {prolog_dir}\n")
    
    # Check if the directory exists
    if not prolog_dir.exists():
        print(f"ERROR: Prolog integration directory not found: {prolog_dir}")
        return
    
    # Check if load_all.pl exists
    load_all_path = prolog_dir / "load_all.pl"
    if not load_all_path.exists():
        print(f"ERROR: load_all.pl not found at {load_all_path}")
        return
    
    # Read and analyze load_all.pl
    print(f"Analyzing load_all.pl...")
    with open(load_all_path, 'r', encoding='utf-8') as f:
        load_all_content = f.read()
    
    # Extract loaded files
    loaded_files = re.findall(r':- consult\(([^)]+)\)', load_all_content)
    print(f"Files loaded in load_all.pl: {loaded_files}\n")
    
    # Check if each file exists
    total_frames = 0
    for file in loaded_files:
        file_path = prolog_dir / f"{file}.pl"
        if file_path.exists():
            frame_count = count_frames(file_path)
            print(f"✓ File exists: {file}.pl - Contains {frame_count} frame definitions")
            total_frames += frame_count
        else:
            print(f"✗ File does not exist: {file}.pl")
    
    print(f"\nTotal frames across all files: {total_frames}\n")
    
    # Check for pea_updates.pl specifically
    pea_updates_path = prolog_dir / "pea_updates.pl"
    if pea_updates_path.exists():
        print("\n----- PEA UPDATES ANALYSIS -----\n")
        analyze_pea_file(pea_updates_path)
    
    # Check for advanced_queries.pl
    advanced_queries_path = prolog_dir / "advanced_queries.pl"
    if advanced_queries_path.exists():
        print("\n----- ADVANCED QUERIES ANALYSIS -----\n")
        analyze_advanced_queries(advanced_queries_path)
    
    # Check for crop_updates.pl to see if potato information is there
    crop_updates_path = prolog_dir / "crop_updates.pl"
    if crop_updates_path.exists():
        print("\n----- CROP UPDATES ANALYSIS -----\n")
        analyze_crop_updates(crop_updates_path)
    
    print("\n===== TEST COMPLETED SUCCESSFULLY =====\n")

def count_frames(file_path):
    """Count frames in a Prolog file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count frame definitions
        frame_count = content.count("frame(")
        return frame_count
    except Exception as e:
        print(f"Error analyzing {file_path}: {str(e)}")
        return 0

def analyze_pea_file(file_path):
    """Analyze the pea_updates.pl file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count pea-specific pests
        pea_pests = re.findall(r'frame\(pest,\s*\[\s*name:\s*([^,]+)', content)
        print(f"Pests defined ({len(pea_pests)}):")
        for pest in pea_pests:
            print(f"  - {pest}")
        
        # Count pea-specific practices
        pea_practices = re.findall(r'frame\(practice,\s*\[\s*name:\s*([^,]+)', content)
        print(f"\nPractices defined ({len(pea_practices)}):")
        for practice in pea_practices:
            print(f"  - {practice}")
        
        # Count pea-specific diseases
        pea_diseases = re.findall(r'frame\(disease,\s*\[\s*name:\s*([^,]+)', content)
        print(f"\nDiseases defined ({len(pea_diseases)}):")
        for disease in pea_diseases:
            print(f"  - {disease}")
    except Exception as e:
        print(f"Error analyzing pea file: {str(e)}")

def analyze_advanced_queries(file_path):
    """Analyze the advanced_queries.pl file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for process_query predicate
        if "process_query" in content:
            print("✓ Contains process_query predicate")
        else:
            print("✗ Missing process_query predicate")
        
        # Count synonym mappings
        synonym_mappings = re.findall(r'synonym_mapping\(([^,]+),\s*([^)]+)\)', content)
        print(f"\nSynonym mappings found: {len(synonym_mappings)}")
        for i, (term1, term2) in enumerate(synonym_mappings[:10]):
            print(f"  - {term1} -> {term2}")
        if len(synonym_mappings) > 10:
            print(f"  - ... and {len(synonym_mappings) - 10} more")
        
        # Check for query intent handlers
        intent_handlers = re.findall(r'identify_query_intent\(([^,]+),\s*([^)]+)\)', content)
        print(f"\nQuery intent handlers: {len(intent_handlers)}")
        for i, (terms, intent) in enumerate(intent_handlers):
            print(f"  - {intent}")
        
        # Check for execute_query predicates
        execute_queries = re.findall(r'execute_query\(([^,]+),\s*([^)]+)\)', content)
        print(f"\nExecute query predicates: {len(execute_queries)}")
        for i, (query_type, _) in enumerate(execute_queries):
            print(f"  - {query_type}")
    except Exception as e:
        print(f"Error analyzing advanced queries file: {str(e)}")

def analyze_crop_updates(file_path):
    """Analyze the crop_updates.pl file for potato information"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for potato-related entries
        potato_mentions = content.lower().count("potato")
        print(f"Potato mentions: {potato_mentions}")
        
        # Count potato-specific pests
        potato_pests = re.findall(r'frame\(pest,\s*\[\s*name:[^,]*potato[^,]*', content, re.IGNORECASE)
        print(f"\nPotato pests defined: {len(potato_pests)}")
        
        # Count potato-specific practices
        potato_practices = re.findall(r'frame\(practice,\s*\[\s*name:[^,]*potato[^,]*', content, re.IGNORECASE)
        print(f"Potato practices defined: {len(potato_practices)}")
        
        # Count potato-specific diseases
        potato_diseases = re.findall(r'frame\(disease,\s*\[\s*name:[^,]*potato[^,]*', content, re.IGNORECASE)
        print(f"Potato diseases defined: {len(potato_diseases)}")
        
        # Look for potato in controls
        potato_controls = re.findall(r'controls:[^]]*potato[^]]*', content, re.IGNORECASE)
        print(f"Entries with potato in controls: {len(potato_controls)}")
    except Exception as e:
        print(f"Error analyzing crop updates file: {str(e)}")

if __name__ == "__main__":
    test_prolog_knowledge_base() 