"""
Manual test script for the Modelfiles integration in the FarmLore system.
This script doesn't rely on external dependencies and focuses on verifying:
1. The existence and content of Modelfiles
2. The OllamaHandler's specialized model mappings
"""
import os
import sys
import json

# Define the path to the modelfiles directory
MODELFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelfiles")

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def test_modelfiles_exist():
    """Test that all required Modelfiles exist and have the expected content."""
    print_separator("TESTING MODELFILES EXISTENCE")
    
    expected_modelfiles = [
        'pest_identification.modelfile',
        'pest_management.modelfile',
        'indigenous_knowledge.modelfile',
        'crop_pests.modelfile',
        'general_query.modelfile'
    ]
    
    all_passed = True
    
    for modelfile in expected_modelfiles:
        modelfile_path = os.path.join(MODELFILES_DIR, modelfile)
        exists = os.path.exists(modelfile_path)
        
        print(f"Checking {modelfile}... ", end="")
        
        if exists:
            print("PASS EXISTS")
            
            # Check file content
            with open(modelfile_path, 'r') as f:
                content = f.read()
                has_from = "FROM" in content
                has_system = "SYSTEM" in content
                has_parameter = "PARAMETER" in content
                
                print(f"  - Has FROM directive: {'PASS' if has_from else 'FAIL'}")
                print(f"  - Has SYSTEM directive: {'PASS' if has_system else 'FAIL'}")
                print(f"  - Has PARAMETER directive: {'PASS' if has_parameter else 'FAIL'}")
                
                if not (has_from and has_system):
                    all_passed = False
                    print(f"  WARNING WARNING: {modelfile} is missing required directives")
                
                # Print the first few lines of the file
                print(f"  - First 3 lines:")
                for i, line in enumerate(content.split('\n')[:3]):
                    print(f"    {i+1}: {line}")
                print("    ...")
        else:
            all_passed = False
            print("FAIL MISSING")
    
    print(f"\nOverall result: {'PASS PASSED' if all_passed else 'FAIL FAILED'}")
    return all_passed

def test_specialized_model_mappings():
    """Test the specialized model mappings that would be used in OllamaHandler."""
    print_separator("TESTING SPECIALIZED MODEL MAPPINGS")
    
    expected_mappings = {
        'pest_identification': 'farmlore-pest-id',
        'pest_management': 'farmlore-pest-mgmt',
        'indigenous_knowledge': 'farmlore-indigenous',
        'crop_pests': 'farmlore-crop-pests',
        'general_query': 'farmlore-general'
    }
    
    expected_paths = {
        'farmlore-pest-id': os.path.join(MODELFILES_DIR, 'pest_identification.modelfile'),
        'farmlore-pest-mgmt': os.path.join(MODELFILES_DIR, 'pest_management.modelfile'),
        'farmlore-indigenous': os.path.join(MODELFILES_DIR, 'indigenous_knowledge.modelfile'),
        'farmlore-crop-pests': os.path.join(MODELFILES_DIR, 'crop_pests.modelfile'),
        'farmlore-general': os.path.join(MODELFILES_DIR, 'general_query.modelfile')
    }
    
    print("Expected specialized model mappings:")
    for query_type, model_name in expected_mappings.items():
        print(f"  - {query_type}: {model_name}")
    
    print("\nExpected modelfile paths:")
    for model_name, path in expected_paths.items():
        exists = os.path.exists(path)
        print(f"  - {model_name}: {path} {'PASS' if exists else 'FAIL'}")
    
    # Check if all paths exist
    all_paths_exist = all(os.path.exists(path) for path in expected_paths.values())
    print(f"\nAll modelfile paths exist: {'PASS PASSED' if all_paths_exist else 'FAIL FAILED'}")
    
    return all_paths_exist

def test_hybrid_engine_usage():
    """Simulate how the HybridEngine would use specialized models."""
    print_separator("SIMULATING HYBRID ENGINE USAGE")
    
    query_types = [
        "pest_identification",
        "control_methods",
        "crop_pests",
        "indigenous_knowledge",
        "general_query"
    ]
    
    specialized_models = {
        'pest_identification': 'farmlore-pest-id',
        'pest_management': 'farmlore-pest-mgmt',
        'indigenous_knowledge': 'farmlore-indigenous',
        'crop_pests': 'farmlore-crop-pests',
        'general_query': 'farmlore-general'
    }
    
    # Map control_methods to pest_management
    if "control_methods" not in specialized_models:
        specialized_models["control_methods"] = specialized_models["pest_management"]
    
    print("Simulating query processing in HybridEngine:")
    for query_type in query_types:
        model = specialized_models.get(query_type, "default-model")
        print(f"  - Query type '{query_type}' would use model '{model}'")
    
    return True

def main():
    """Run all tests."""
    print("Starting manual tests for Modelfiles integration...")
    
    tests = [
        test_modelfiles_exist,
        test_specialized_model_mappings,
        test_hybrid_engine_usage
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print_separator("TEST SUMMARY")
    for i, (test, result) in enumerate(zip(tests, results)):
        print(f"Test {i+1}: {test.__name__} - {'PASS PASSED' if result else 'FAIL FAILED'}")
    
    overall_result = all(results)
    print(f"\nOverall result: {'PASS ALL TESTS PASSED' if overall_result else 'FAIL SOME TESTS FAILED'}")

if __name__ == "__main__":
    main()
