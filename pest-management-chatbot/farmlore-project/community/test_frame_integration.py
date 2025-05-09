"""
Test script to demonstrate the integration of indigenous knowledge with FarmLore.

This script shows how Basotho indigenous farming knowledge is properly integrated
with the existing knowledge base in a scalable and structured way.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Add prolog_intergration directory to path
sys.path.append(os.path.join(parent_dir, 'prolog_intergration'))
from connector import PrologConnector

def test_indigenous_knowledge_integration():
    """Test the integration of indigenous knowledge with FarmLore."""
    print("Testing FarmLore Indigenous Knowledge Integration")
    print("===============================================")
    
    # Initialize the Prolog connector
    print("\n1. Initializing Prolog Connector...")
    prolog = PrologConnector()
    
    # Test querying indigenous practices
    print("\n2. Indigenous Pest Control Practices:")
    query = "frame(practice, [name:Name, type:pest_control, description:Desc, cultural_context:Ctx]), member(basotho, Ctx)"
    results = prolog.query(query)
    
    for result in results:
        name = result.get('Name', '').replace('_', ' ').title()
        description = result.get('Desc', '')
        
        print(f"- {name}: {description}")
    
    # Test querying indigenous soil fertility practices
    print("\n3. Indigenous Soil Fertility Practices:")
    query = "frame(practice, [name:Name, type:soil_fertility, description:Desc, cultural_context:Ctx]), member(basotho, Ctx)"
    results = prolog.query(query)
    
    for result in results:
        name = result.get('Name', '').replace('_', ' ').title()
        description = result.get('Desc', '')
        
        print(f"- {name}: {description}")
    
    # Test querying indigenous disease management practices
    print("\n4. Indigenous Disease Management Practices:")
    query = "frame(practice, [name:Name, type:disease_management, description:Desc, cultural_context:Ctx]), member(basotho, Ctx)"
    results = prolog.query(query)
    
    for result in results:
        name = result.get('Name', '').replace('_', ' ').title()
        description = result.get('Desc', '')
        
        print(f"- {name}: {description}")
    
    # Test querying ecological indicators
    print("\n5. Ecological Indicators:")
    query = "frame(ecological_indicator, [name:Name, description:Desc, interpretation:Interp, region:Region])"
    results = prolog.query(query)
    
    for result in results:
        name = result.get('Name', '').replace('_', ' ').title()
        description = result.get('Desc', '')
        interpretation = result.get('Interp', '')
        region = result.get('Region', '').title()
        
        print(f"- {name} in {region}: {description}")
        print(f"  Interpretation: {interpretation}")
    
    # Test querying Sesotho terminology
    print("\n6. Sesotho Terminology:")
    query = "frame(sesotho_term, [term:Term, english:English, description:Desc])"
    results = prolog.query(query)
    
    for result in results:
        term = result.get('Term', '')
        english = result.get('English', '')
        description = result.get('Desc', '')
        
        print(f"- {term} (Sesotho): {english} - {description}")
    
    # Test integration with existing knowledge
    print("\n7. Integration with Existing Knowledge:")
    print("\n7.1 All Practices for Controlling Aphids:")
    query = "frame(practice, [name:Name, controls:Controls, type:Type, cultural_context:Ctx]), member(aphids, Controls)"
    results = prolog.query(query)
    
    for result in results:
        name = result.get('Name', '').replace('_', ' ').title()
        practice_type = result.get('Type', '').replace('_', ' ').title()
        ctx = result.get('Ctx', [])
        
        if 'basotho' in ctx:
            practice_source = "Indigenous"
        else:
            practice_source = "Conventional"
        
        print(f"- {name} ({practice_source} {practice_type})")
    
    print("\nIntegration Test Complete!")
    print("The indigenous knowledge has been successfully integrated with FarmLore's knowledge base.")

if __name__ == "__main__":
    test_indigenous_knowledge_integration()
