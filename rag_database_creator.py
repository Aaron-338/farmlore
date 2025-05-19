#!/usr/bin/env python
"""
RAG Database Creator

This script creates a vector database for Retrieval-Augmented Generation (RAG)
with agricultural pest management information.
"""
import os
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("rag_database_creator")

# Sample pest management data
PEST_DATA = [
    {
        "title": "Aphid Control on Tomatoes",
        "content": """
Aphids are common pests on tomato plants. They are small, soft-bodied insects that can be green, yellow, brown, red, or black. They feed on plant sap and can cause stunted growth, yellowed leaves, and reduced yields.

Effective control methods for aphids on tomatoes include:

1. Biological control: Introduce natural predators like ladybugs, lacewings, and parasitic wasps that feed on aphids.

2. Neem oil: Apply neem oil spray, which disrupts the aphid life cycle and acts as a repellent.

3. Insecticidal soap: Use insecticidal soap sprays that are specifically designed for soft-bodied insects like aphids.

4. Water spray: Use a strong stream of water to physically remove aphids from plants.

5. Companion planting: Plant aphid-repelling plants like marigolds, nasturtiums, and garlic near tomatoes.

6. Diatomaceous earth: Apply food-grade diatomaceous earth around plants to control aphid populations.

7. Pruning: Remove heavily infested leaves and stems to prevent spread.

8. Aluminum foil mulch: Place aluminum foil around the base of plants to repel aphids with reflective light.

For severe infestations, organic or synthetic insecticides may be necessary, but always follow label instructions and consider the environmental impact.
"""
    },
    {
        "title": "Spider Mite Management in Gardens",
        "content": """
Spider mites are tiny arachnids that can cause significant damage to garden plants. They appear as tiny moving dots, often red, brown, or yellow. Signs of infestation include fine webbing on plants and stippled, discolored leaves.

Effective management strategies include:

1. Water spray: Regular, forceful spraying with water can dislodge mites and reduce populations.

2. Increase humidity: Spider mites thrive in dry conditions, so increasing humidity can discourage them.

3. Neem oil: Apply neem oil as a natural miticide that disrupts the spider mite life cycle.

4. Insecticidal soap: Use specifically formulated soaps that are effective against mites but gentle on plants.

5. Predatory mites: Introduce beneficial predatory mites that feed on spider mites.

6. Proper plant spacing: Ensure good air circulation between plants to prevent infestations.

7. Avoid drought stress: Keep plants well-watered as stressed plants are more susceptible to mite damage.

8. Diatomaceous earth: Apply around plants to control mite populations.

For severe infestations, miticides may be necessary, but rotate different products to prevent resistance development.
"""
    },
    {
        "title": "Controlling Tomato Hornworms",
        "content": """
Tomato hornworms are large, green caterpillars with white stripes and a horn-like projection on their rear end. They can quickly defoliate tomato plants and damage developing fruit.

Effective control methods include:

1. Hand-picking: Regularly inspect plants and manually remove hornworms. Drop them in soapy water or relocate them far from your garden.

2. Bacillus thuringiensis (Bt): Apply this natural bacterial insecticide that specifically targets caterpillars without harming beneficial insects.

3. Parasitic wasps: Encourage or introduce parasitic wasps like Braconid wasps that lay eggs on hornworms.

4. Companion planting: Plant dill, basil, marigold, or borage near tomatoes to repel hornworms or attract beneficial insects.

5. Crop rotation: Change where you plant tomatoes each year to disrupt the life cycle of overwintering pupae.

6. Tilling soil: In fall, till the soil to expose overwintering pupae to predators and cold temperatures.

7. Row covers: Use lightweight row covers to prevent adult moths from laying eggs on plants.

8. Black light traps: Set up black light traps to catch adult moths at night before they lay eggs.

Regular monitoring is key to preventing severe infestations, as hornworms can cause extensive damage quickly.
"""
    },
    {
        "title": "Managing Colorado Potato Beetles",
        "content": """
Colorado potato beetles are striped beetles that feed on potato plants, as well as eggplant and tomatoes. Adults have distinctive yellow and black stripes, while larvae are reddish with black spots.

Effective management approaches include:

1. Hand-picking: Regularly remove adults, larvae, and egg clusters from plants and destroy them.

2. Row covers: Use floating row covers to prevent beetles from reaching plants, removing covers during flowering if pollination is needed.

3. Crop rotation: Rotate nightshade family crops (potatoes, tomatoes, eggplants) to different locations each year.

4. Mulching: Use straw mulch, which creates habitat for predatory insects that feed on the beetles.

5. Neem oil: Apply neem oil as a repellent and growth regulator for the beetles.

6. Spinosad: Use this organic insecticide derived from soil bacteria that is effective against Colorado potato beetles.

7. Beneficial insects: Encourage predatory stink bugs, ladybugs, and lacewings that feed on beetle eggs and larvae.

8. Trap crops: Plant eggplants as trap crops around potato patches, then treat or remove the trap crops when infested.

Monitoring early in the season is crucial, as controlling the first generation prevents larger second-generation populations.
"""
    },
    {
        "title": "Dealing with Squash Bugs in Vegetable Gardens",
        "content": """
Squash bugs are common pests of squash, pumpkins, and other cucurbits. Adults are brownish-black with flat backs, while nymphs are gray with black legs.

Effective control methods include:

1. Monitoring: Check under leaves for characteristic bronze-colored egg clusters and crush them.

2. Trap boards: Place boards near plants; squash bugs will hide under them at night and can be collected in the morning.

3. Row covers: Use until flowering, then remove for pollination.

4. Companion planting: Interplant with nasturtiums, marigolds, or radishes to repel squash bugs.

5. Timing plantings: Plant early or late to avoid peak squash bug season.

6. Diatomaceous earth: Apply around the base of plants to control nymphs.

7. Neem oil or insecticidal soap: Apply to target nymphs, as adults are resistant to many treatments.

8. Clean cultivation: Remove garden debris and old cucurbit plants after harvest to eliminate overwintering sites.

9. Resistant varieties: Choose squash varieties less susceptible to squash bug damage.

Controlling young nymphs is much more effective than trying to manage adult populations, so early detection is key.
"""
    }
]

def create_rag_database(data: List[Dict], persist_dir: str = "./data/chromadb"):
    """Create a RAG vector database from agricultural pest management data"""
    try:
        # Import necessary libraries
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        # Create the directory if it doesn't exist
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Manually prepare documents and texts
        texts = []
        metadatas = []
        
        # Simple text chunking function
        def chunk_text(text, chunk_size=500, overlap=50):
            chunks = []
            start = 0
            text_length = len(text)
            
            while start < text_length:
                end = min(start + chunk_size, text_length)
                if end < text_length and end < start + chunk_size:
                    # Find the last period or newline to break at
                    last_period = text.rfind('.', start, end)
                    last_newline = text.rfind('\n', start, end)
                    break_point = max(last_period, last_newline)
                    
                    if break_point > start:
                        end = break_point + 1
                
                chunks.append(text[start:end])
                start = end - overlap
            
            return chunks
        
        # Process each document
        for item in data:
            # Split content into chunks
            content_chunks = chunk_text(item["content"])
            
            for chunk in content_chunks:
                texts.append(chunk)
                metadatas.append({"title": item["title"]})
        
        logger.info(f"Created {len(texts)} text chunks")
        
        # Create and persist the vector store
        vectorstore = Chroma.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        
        # Persist the vector store
        vectorstore.persist()
        logger.info(f"Successfully created and persisted vector store at {persist_dir}")
        
        # Test a sample query
        test_query = "How do I control aphids on tomatoes?"
        results = vectorstore.similarity_search(test_query, k=2)
        
        logger.info(f"Test query: '{test_query}'")
        logger.info(f"Found {len(results)} results")
        for i, doc in enumerate(results):
            logger.info(f"Result {i+1}: {doc.page_content[:150]}...")
        
        return True
    
    except Exception as e:
        logger.error(f"Error creating RAG database: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== RAG Database Creator ===")
    
    # Get persistence directory from environment or use default
    persist_dir = os.environ.get("RAG_PERSIST_DIR", "./data/chromadb")
    print(f"Creating vector database at: {persist_dir}")
    
    success = create_rag_database(PEST_DATA, persist_dir)
    
    if success:
        print("✅ Successfully created RAG vector database!")
        print("The database now contains information on various pest management techniques.")
        print("You can now use the RAG integration to enhance query responses.")
    else:
        print("❌ Failed to create RAG vector database.")
        print("Check the logs for more information.") 