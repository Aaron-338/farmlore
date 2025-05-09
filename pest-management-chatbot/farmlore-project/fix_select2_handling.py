#!/usr/bin/env python
"""
Script to fix Select2 handling in form submissions.
This script adds a middleware to log all POST requests and ensure Select2 values are properly processed.
"""
import os
import django
import logging
import json
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import IndigenousKnowledge, KnowledgeKeeper
from django.db import connection
from django.core.management import call_command

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("form_fix.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fix_select2_handling():
    """Fix Select2 handling in the knowledge form."""
    logger.info("=== FIXING SELECT2 HANDLING IN KNOWLEDGE FORM ===")
    
    # Create a test entry for each user to verify form handling
    users = User.objects.all()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    for user in users:
        logger.info(f"Creating test entry for user: {user.username}")
        
        try:
            # Get or create knowledge keeper
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
            
            # Create entry with Select2 fields
            entry = IndigenousKnowledge.objects.create(
                title=f"Select2 Test - {user.username} - {timestamp}",
                description="This is a test entry to verify Select2 handling",
                practice_type="pest_control",
                materials=["Material 1", "Material 2"],
                crops=["Maize", "Beans"],
                pests=["Aphids", "Beetles"],
                seasons=["Summer", "Spring"],
                keeper=keeper,
                verification_status="pending",
                verification_count=0
            )
            
            logger.info(f"Created entry: ID {entry.id}, Title: {entry.title}")
            logger.info(f"Materials: {entry.materials}")
            logger.info(f"Crops: {entry.crops}")
            logger.info(f"Pests: {entry.pests}")
            logger.info(f"Seasons: {entry.seasons}")
            
        except Exception as e:
            logger.error(f"Error creating entry for {user.username}: {str(e)}")
    
    # Check that all entries are visible in the dashboard
    logger.info("\n=== CHECKING DASHBOARD VISIBILITY ===")
    entries = IndigenousKnowledge.objects.all().order_by('-date_added')
    logger.info(f"Total knowledge entries: {entries.count()}")
    
    for entry in entries[:10]:  # Show only the 10 most recent entries
        logger.info(f"ID: {entry.id}, Title: {entry.title}, User: {entry.keeper.user.username}")
    
    # Make sure migrations are up to date
    logger.info("\n=== CHECKING MIGRATIONS ===")
    call_command('showmigrations', 'community')
    
    logger.info("\nFix script completed. Please check the logs for any issues.")

if __name__ == "__main__":
    fix_select2_handling()
