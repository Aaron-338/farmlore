"""
Test script to demonstrate the integration of indigenous knowledge with FarmLore.

This script shows how Basotho indigenous farming knowledge is integrated with the chatbot
to provide culturally appropriate pest management advice.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Add inference_engine directory to path
inference_engine_dir = os.path.join(parent_dir, 'api', 'inference_engine')
if inference_engine_dir not in sys.path:
    sys.path.append(inference_engine_dir)

# Import the Prolog engine
from prolog_engine import PrologEngine

def test_indigenous_knowledge():
    """Test the integration of indigenous knowledge with FarmLore."""
    print("Testing FarmLore Indigenous Knowledge Integration")
    print("===============================================")
    
    # Initialize the Prolog engine with the hardcoded knowledge base
    print("\n1. Initializing Prolog Engine with Indigenous Knowledge...")
    prolog = PrologEngine()
    
    # Test querying indigenous pest management methods
    print("\n2. Indigenous Pest Management Methods:")
    query = "indigenous_pest_method(Method), indigenous_method_name(Method, Name), indigenous_method_description(Method, Description)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        description = result.get('Description', '')
        method_id = result.get('Method', '')
        
        print(f"- {method_name}: {description}")
        
        # Get materials for this method
        materials_query = f"indigenous_method_materials({method_id}, Materials)"
        materials_results = prolog.safe_query(materials_query)
        if materials_results:
            materials = materials_results[0].get('Materials', '')
            print(f"  Materials: {materials}")
        
        # Get applicable crops
        crops_query = f"indigenous_method_crop({method_id}, Crop)"
        crops_results = prolog.safe_query(crops_query)
        if crops_results:
            crops = [res.get('Crop', '').replace('_', ' ') for res in crops_results]
            print(f"  Applicable crops: {', '.join(crops)}")
        
        # Get target pests
        pests_query = f"indigenous_method_pest({method_id}, Pest)"
        pests_results = prolog.safe_query(pests_query)
        if pests_results:
            pests = [res.get('Pest', '').replace('_', ' ') for res in pests_results]
            print(f"  Target pests: {', '.join(pests)}")
        
        print()
    
    # Test querying indigenous soil methods
    print("\n3. Indigenous Soil Fertilization Methods:")
    query = "indigenous_soil_method(Method), indigenous_method_name(Method, Name), indigenous_method_description(Method, Description)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        description = result.get('Description', '')
        method_id = result.get('Method', '')
        
        print(f"- {method_name}: {description}")
        
        # Get materials for this method
        materials_query = f"indigenous_method_materials({method_id}, Materials)"
        materials_results = prolog.safe_query(materials_query)
        if materials_results:
            materials = materials_results[0].get('Materials', '')
            print(f"  Materials: {materials}")
        
        # Get applicable crops
        crops_query = f"indigenous_method_crop({method_id}, Crop)"
        crops_results = prolog.safe_query(crops_query)
        if crops_results:
            crops = [res.get('Crop', '').replace('_', ' ') for res in crops_results]
            print(f"  Applicable crops: {', '.join(crops)}")
        
        print()
    
    # Test finding indigenous methods for specific pests
    print("\n4. Indigenous Methods for Controlling Aphids:")
    query = "indigenous_method_pest(Method, aphid), indigenous_method_name(Method, Name)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        print(f"- {method_name}")
    
    # Test finding indigenous methods for specific crops
    print("\n5. Indigenous Methods for Tomato Crops:")
    query = "indigenous_method_crop(Method, tomato), indigenous_method_name(Method, Name)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        print(f"- {method_name}")
    
    # Test integration with existing knowledge base
    print("\n6. Integration with Existing Knowledge Base:")
    
    # Test finding all methods (indigenous and conventional) for controlling aphids
    print("\n6.1 All Methods for Controlling Aphids:")
    
    # First get conventional methods
    query = "control_method(aphid, Method)"
    conventional_results = prolog.safe_query(query)
    conventional_methods = [res.get('Method', '').replace('_', ' ') for res in conventional_results]
    
    # Then get indigenous methods
    query = "indigenous_method_pest(Method, aphid), indigenous_method_name(Method, Name)"
    indigenous_results = prolog.safe_query(query)
    indigenous_methods = [res.get('Name', '') for res in indigenous_results]
    
    print("Conventional methods:")
    for method in conventional_methods:
        print(f"- {method}")
    
    print("\nIndigenous methods:")
    for method in indigenous_methods:
        print(f"- {method}")
    
    # Test finding all methods for protecting tomato crops
    print("\n6.2 All Methods for Protecting Tomato Crops:")
    
    # Get pests that affect tomatoes
    query = "affects(Pest, tomato)"
    pest_results = prolog.safe_query(query)
    tomato_pests = [res.get('Pest', '') for res in pest_results]
    
    print(f"Tomato is affected by {len(tomato_pests)} pests:")
    for pest in tomato_pests:
        print(f"- {pest}")
        
        # Get conventional control methods
        control_query = f"control_method({pest}, Method)"
        control_results = prolog.safe_query(control_query)
        if control_results:
            methods = [res.get('Method', '').replace('_', ' ') for res in control_results]
            print(f"  Conventional control methods: {', '.join(methods)}")
        
        # Get indigenous control methods
        indigenous_query = f"indigenous_method_pest(Method, {pest}), indigenous_method_name(Method, Name)"
        indigenous_results = prolog.safe_query(indigenous_query)
        if indigenous_results:
            methods = [res.get('Name', '') for res in indigenous_results]
            print(f"  Indigenous control methods: {', '.join(methods)}")
    
    # Show benefits of integration
    print("\n7. Benefits of Indigenous Knowledge Integration:")
    print("- Preserves and promotes Basotho indigenous technical knowledge")
    print("- Provides culturally appropriate solutions to farming challenges")
    print("- Validates traditional practices through community verification")
    print("- Creates a living knowledge base that grows with community input")
    print("- Enhances the chatbot's ability to provide relevant advice to Basotho farmers")
    print("- Fosters community engagement and knowledge sharing")

if __name__ == "__main__":
    test_indigenous_knowledge()
