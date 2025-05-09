"""Test script to verify our setup is working correctly."""
import spacy
from pyswip import Prolog
import os

def test_spacy():
    """Test if spaCy is working with the English model."""
    try:
        nlp = spacy.load('en_core_web_sm')
        test_text = "What pests affect tomatoes and how can I control them?"
        doc = nlp(test_text)
        print("\nSpaCy Test:")
        print("✓ Successfully loaded spaCy model")
        print("Tokens:", [token.text for token in doc])
        print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
        return True
    except Exception as e:
        print("× Error loading spaCy:", str(e))
        return False

def test_prolog():
    """Test if Prolog integration is working."""
    try:
        prolog = Prolog()
        kb_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'knowledge_base',
            'pest_kb.pl'
        )
        prolog.consult(kb_path)
        print("\nProlog Test:")
        print("✓ Successfully loaded Prolog")
        
        # Test a simple query
        print("Testing query: pests_for_crop(tomato, Pests)")
        results = list(prolog.query("pests_for_crop(tomato, Pests)"))
        if results:
            print("✓ Successfully queried knowledge base")
            print("Found pests:", results[0]['Pests'])
        else:
            print("Query returned no results")
        return True
    except Exception as e:
        print("× Error with Prolog:", str(e))
        return False

if __name__ == "__main__":
    print("Testing NLP and Prolog Setup...")
    spacy_ok = test_spacy()
    prolog_ok = test_prolog()
    
    if spacy_ok and prolog_ok:
        print("\n✓ All components working correctly!")
    else:
        print("\n× Some components failed. Please check the errors above.")
