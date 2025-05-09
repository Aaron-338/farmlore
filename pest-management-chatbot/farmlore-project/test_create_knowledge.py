#!/usr/bin/env python
"""
Test script to create a knowledge entry for a specific user.
This script will create a knowledge entry for the specified user to test visibility.
"""
import os
import sys
import django
import logging
import time

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import KnowledgeKeeper, IndigenousKnowledge

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_knowledge_for_user(username):
    """Create a knowledge entry for the specified user."""
    try:
        # Get the user
        user = User.objects.get(username=username)
        logger.info(f"Found user: {user.username} (ID: {user.id})")
        
        # Get or create knowledge keeper profile
        try:
            keeper = user.knowledge_keeper
            logger.info(f"Found existing keeper: {keeper}")
        except KnowledgeKeeper.DoesNotExist:
            keeper = KnowledgeKeeper.objects.create(
                user=user,
                village="Test Village",
                district="Test District",
                years_experience=5
            )
            logger.info(f"Created new keeper: {keeper}")
        
        # Create a knowledge entry
        timestamp = int(time.time())
        entry = IndigenousKnowledge.objects.create(
            title=f"Test Entry by {username} - {timestamp}",
            description=f"This is a test entry created by {username} to verify visibility.",
            practice_type="pest_control",
            materials=["Test material 1", "Test material 2"],
            crops=["Maize", "Beans"],
            pests=["Aphids", "Beetles"],
            seasons=["Summer", "Spring"],
            keeper=keeper,
            verification_status="pending",
            verification_count=0
        )
        
        logger.info(f"Created knowledge entry: ID {entry.id}, Title: {entry.title}")
        logger.info(f"Entry keeper: {entry.keeper} (User: {user.username})")
        
        return entry
    except User.DoesNotExist:
        logger.error(f"User {username} not found!")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python test_create_knowledge.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    logger.info(f"Creating knowledge entry for user: {username}")
    
    entry = create_knowledge_for_user(username)
    
    if entry:
        logger.info("Successfully created knowledge entry")
    else:
        logger.error("Failed to create knowledge entry")
