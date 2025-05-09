#!/usr/bin/env python
"""
Debug script to check knowledge entry visibility.
This script checks if knowledge entries are visible to all users.
"""
import os
import django
import logging
import json

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import IndigenousKnowledge, KnowledgeKeeper

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_knowledge_entries():
    """Check all knowledge entries in the database."""
    entries = IndigenousKnowledge.objects.all().order_by('-date_added')
    logger.info(f"Total knowledge entries: {entries.count()}")
    
    # Print details of each entry
    for entry in entries:
        logger.info(f"ID: {entry.id}, Title: {entry.title}, Status: {entry.verification_status}")
        logger.info(f"  Keeper: {entry.keeper}, Added: {entry.date_added}")
        logger.info(f"  Materials: {json.dumps(entry.materials)}")
        logger.info(f"  Crops: {json.dumps(entry.crops)}")
        logger.info(f"  Pests: {json.dumps(entry.pests)}")
        logger.info(f"  Seasons: {json.dumps(entry.seasons)}")
        logger.info("---")

def check_users_and_keepers():
    """Check all users and knowledge keepers."""
    users = User.objects.all()
    logger.info(f"Total users: {users.count()}")
    
    for user in users:
        logger.info(f"User: {user.username}, ID: {user.id}")
        try:
            keeper = user.knowledge_keeper
            logger.info(f"  Keeper: {keeper}, Village: {keeper.village}")
            
            # Check entries for this keeper
            entries = IndigenousKnowledge.objects.filter(keeper=keeper)
            logger.info(f"  Entries: {entries.count()}")
            for entry in entries:
                logger.info(f"    - {entry.title} (ID: {entry.id})")
        except KnowledgeKeeper.DoesNotExist:
            logger.info("  No keeper profile")
        logger.info("---")

if __name__ == "__main__":
    logger.info("=== CHECKING KNOWLEDGE ENTRIES ===")
    check_knowledge_entries()
    
    logger.info("\n=== CHECKING USERS AND KEEPERS ===")
    check_users_and_keepers()
