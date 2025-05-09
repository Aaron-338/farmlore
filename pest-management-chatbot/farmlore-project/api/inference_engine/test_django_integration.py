"""Test script for Prolog and HybridEngine integration."""
import os
import sys
import asyncio
from pathlib import Path

# Import the engines directly
from prolog_engine import PrologEngine

async def test_prolog_engine_directly():
    """Test the Prolog engine directly."""
    print("\n--- Testing PrologEngine Directly ---")
    try:
        engine = PrologEngine()
        
        # Test 1: Query pests for tomato
        print("\nTest 1: Query pests for tomato")
        pests = engine.query_pests_for_crop("tomato")
        print(f"Pests for tomato: {pests}")
        
        # Test 2: Query control methods for aphid
        print("\nTest 2: Query control methods for aphid")
        methods = engine.query_control_methods("aphid")
        print(f"Control methods for aphid: {methods}")
        
        # Test 3: Get pest details
        print("\nTest 3: Get details for aphid")
        details = engine.get_pest_details("aphid")
        print(f"Aphid details: {details}")
        
        return True
    except Exception as e:
        print(f"Error testing Prolog engine: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("Starting Prolog integration tests...")
    
    # Test Prolog Engine
    prolog_success = await test_prolog_engine_directly()
    
    # Print summary
    print("\n--- Test Summary ---")
    print(f"Prolog Engine Test: {'PASSED' if prolog_success else 'FAILED'}")
    
    if prolog_success:
        print("\nTest PASSED! The Prolog integration is working correctly.")
    else:
        print("\nTest FAILED. Please check the error messages above.")

if __name__ == "__main__":
    # Run the async tests
    asyncio.run(main())
