#!/usr/bin/env python
"""
Test script to verify knowledge entry visibility.
This script creates a new knowledge entry and verifies it's visible in the database.
"""
import os
import sys
import django
import logging
import random
import time

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import KnowledgeKeeper, IndigenousKnowledge
from django.utils import timezone

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_knowledge_entry():
    """Create a test knowledge entry with a unique title."""
    # Get or create a test user
    username = 'testuser'
    try:
        user = User.objects.get(username=username)
        logger.info(f"Found existing user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        logger.info(f"Created new user: {user.username}")
    
    # Get or create a knowledge keeper profile
    try:
        keeper = user.knowledge_keeper
        logger.info(f"Found existing knowledge keeper: {keeper}")
    except KnowledgeKeeper.DoesNotExist:
        keeper = KnowledgeKeeper.objects.create(
            user=user,
            village='Test Village',
            district='Test District',
            years_experience=10,
            specialization='Test Specialization',
            bio='Test bio'
        )
        logger.info(f"Created new knowledge keeper: {keeper}")
    
    # Create a unique title with timestamp
    timestamp = int(time.time())
    title = f"Test Knowledge Entry {timestamp}"
    
    # Create the knowledge entry
    entry = IndigenousKnowledge.objects.create(
        title=title,
        description="This is a test knowledge entry to verify visibility in the dashboard.",
        practice_type='pest_control',
        materials=['Test material 1', 'Test material 2'],
        crops=['Maize', 'Beans'],
        pests=['Aphids', 'Beetles'],
        seasons=['Summer', 'Spring'],
        keeper=keeper,
        verification_status='pending',
        verification_count=0
    )
    
    logger.info(f"Created new knowledge entry: {entry.id} - {entry.title}")
    return entry

def verify_entry_visibility(entry_id):
    """Verify that the entry is visible in the database."""
    try:
        entry = IndigenousKnowledge.objects.get(id=entry_id)
        logger.info(f"Entry found in database: {entry.id} - {entry.title}")
        
        # Get all entries to verify it's included in the queryset
        all_entries = IndigenousKnowledge.objects.all().order_by('-date_added')
        logger.info(f"Total entries in database: {all_entries.count()}")
        
        # Check if our entry is in the first page (assuming 10 per page)
        first_page = all_entries[:10]
        found = any(e.id == entry_id for e in first_page)
        
        if found:
            logger.info(f"Entry {entry_id} is visible in the first page of results")
        else:
            logger.warning(f"Entry {entry_id} is NOT visible in the first page of results")
            
        # Print all entries in the database for debugging
        logger.info("All entries in database:")
        for e in all_entries:
            logger.info(f"ID: {e.id}, Title: {e.title}, Status: {e.verification_status}, Keeper: {e.keeper}")
        
        return found
    except IndigenousKnowledge.DoesNotExist:
        logger.error(f"Entry {entry_id} not found in database!")
        return False

if __name__ == "__main__":
    logger.info("Starting knowledge visibility test")
    
    # Create a test entry
    entry = create_test_knowledge_entry()
    
    # Verify it's visible
    visible = verify_entry_visibility(entry.id)
    
    if visible:
        logger.info("TEST PASSED: Entry is visible in the database")
    else:
        logger.error("TEST FAILED: Entry is not visible in the database")
    
    logger.info("Test completed")
