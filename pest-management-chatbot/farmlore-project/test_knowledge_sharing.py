#!/usr/bin/env python
"""
Test script to diagnose issues with knowledge sharing in the FarmLore community app.
This script will:
1. Create a test user if needed
2. Create a knowledge keeper profile if needed
3. Submit a test knowledge entry
4. Check if it appears in the database
"""
import os
import sys
import django
import logging
import json
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now import Django models
from django.contrib.auth.models import User
from community.models import KnowledgeKeeper, IndigenousKnowledge, CommunityValidation
from django.db import transaction

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_user():
    """Create a test user if it doesn't exist"""
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'testpassword123'
    
    try:
        user = User.objects.get(username=username)
        logger.info(f"Test user '{username}' already exists")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
        logger.info(f"Created test user '{username}'")
    
    return user

def create_knowledge_keeper(user):
    """Create a knowledge keeper profile for the user if it doesn't exist"""
    try:
        keeper = user.knowledge_keeper
        logger.info(f"Knowledge keeper profile for {user.username} already exists")
    except KnowledgeKeeper.DoesNotExist:
        keeper = KnowledgeKeeper.objects.create(
            user=user,
            village='Test Village',
            district='Test District',
            years_experience=10,
            specialization='Pest Control',
            bio='Test knowledge keeper for debugging purposes'
        )
        logger.info(f"Created knowledge keeper profile for {user.username}")
    
    return keeper

def create_test_knowledge_entry(keeper):
    """Create a test knowledge entry"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    try:
        with transaction.atomic():
            entry = IndigenousKnowledge.objects.create(
                title=f'Test Knowledge Entry {timestamp}',
                description='This is a test knowledge entry created for debugging purposes.',
                practice_type='pest_control',
                materials=['Ash', 'Water', 'Chili peppers'],
                crops=['maize', 'beans', 'tomato'],
                pests=['aphids', 'spider_mites'],
                seasons=['summer', 'growing_season'],
                keeper=keeper,
                verification_status='pending',
                verification_count=0
            )
            logger.info(f"Created test knowledge entry: {entry.title} (ID: {entry.id})")
            return entry
    except Exception as e:
        logger.error(f"Error creating knowledge entry: {str(e)}")
        return None

def check_knowledge_entry(entry_id):
    """Check if a knowledge entry exists and print its details"""
    try:
        entry = IndigenousKnowledge.objects.get(id=entry_id)
        logger.info(f"Found knowledge entry: {entry.title} (ID: {entry.id})")
        logger.info(f"Verification status: {entry.verification_status}")
        logger.info(f"Verification count: {entry.verification_count}")
        logger.info(f"Date added: {entry.date_added}")
        logger.info(f"Materials: {entry.materials}")
        logger.info(f"Crops: {entry.crops}")
        logger.info(f"Pests: {entry.pests}")
        logger.info(f"Seasons: {entry.seasons}")
        return entry
    except IndigenousKnowledge.DoesNotExist:
        logger.error(f"Knowledge entry with ID {entry_id} does not exist")
        return None

def list_recent_entries():
    """List the 5 most recent knowledge entries"""
    entries = IndigenousKnowledge.objects.all().order_by('-date_added')[:5]
    logger.info(f"Found {entries.count()} recent knowledge entries:")
    for entry in entries:
        logger.info(f"- {entry.title} (ID: {entry.id}, Status: {entry.verification_status}, Added: {entry.date_added})")
    return entries

def main():
    """Main function"""
    logger.info("Starting knowledge sharing test")
    
    # Create test user and knowledge keeper
    user = create_test_user()
    keeper = create_knowledge_keeper(user)
    
    # Create test knowledge entry
    entry = create_test_knowledge_entry(keeper)
    
    if entry:
        # Check the entry
        check_knowledge_entry(entry.id)
    
    # List recent entries
    list_recent_entries()
    
    logger.info("Knowledge sharing test completed")

if __name__ == '__main__':
    main()
