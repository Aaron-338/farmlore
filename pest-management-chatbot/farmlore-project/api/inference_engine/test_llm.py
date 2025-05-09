"""Test script for the Ollama LLM handler."""
import asyncio
from llm_handler import OllamaHandler

async def test_basic_generation():
    """Test basic response generation."""
    llm = OllamaHandler()
    prompt = "What are common pests that affect tomato plants?"
    print("\nTesting basic generation...")
    try:
        response = await llm.generate_response(prompt)
        print("✓ Successfully generated response:")
        print(response)
        return True
    except Exception as e:
        print("× Error generating response:", str(e))
        return False

async def test_prolog_enhancement():
    """Test enhancing Prolog results."""
    llm = OllamaHandler()
    prolog_result = {
        "pest": "tomato_hornworm",
        "symptoms": ["defoliation", "fruit_damage"],
        "controls": ["handpicking", "bt_spray"]
    }
    user_query = "How do I deal with tomato hornworms?"
    
    print("\nTesting Prolog result enhancement...")
    try:
        response = await llm.enhance_prolog_response(
            prolog_result,
            user_query,
            crop_name="tomato"
        )
        print("✓ Successfully enhanced Prolog response:")
        print(response)
        return True
    except Exception as e:
        print("× Error enhancing Prolog response:", str(e))
        return False

async def test_pest_analysis():
    """Test pest analysis generation."""
    llm = OllamaHandler()
    symptoms = ["yellowing leaves", "sticky residue", "stunted growth"]
    crop = "tomato"
    prolog_matches = ["aphids", "whiteflies"]
    
    print("\nTesting pest analysis...")
    try:
        response = await llm.get_pest_analysis(symptoms, crop, prolog_matches)
        print("✓ Successfully generated pest analysis:")
        print(response)
        return True
    except Exception as e:
        print("× Error generating pest analysis:", str(e))
        return False

async def main():
    """Run all tests."""
    print("Testing LLM Handler...")
    
    basic_ok = await test_basic_generation()
    enhance_ok = await test_prolog_enhancement()
    analysis_ok = await test_pest_analysis()
    
    if all([basic_ok, enhance_ok, analysis_ok]):
        print("\n✓ All LLM tests completed successfully!")
    else:
        print("\n× Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
