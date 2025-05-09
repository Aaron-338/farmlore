#!/usr/bin/env python
"""
Debug script to fix form submission issues.
This script will simulate a form submission and diagnose any issues.
"""
import os
import django
import logging
import time
import json
import traceback
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import IndigenousKnowledge, KnowledgeKeeper
from django.db import transaction, connection, reset_queries
from django.conf import settings

# Enable query logging
settings.DEBUG = True

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulate_form_submission(username, title, description):
    """Simulate a form submission and diagnose any issues."""
    logger.info(f"Simulating form submission for user: {username}")
    
    # Get the user
    try:
        user = User.objects.get(username=username)
        logger.info(f"Found user: {user.username} (ID: {user.id})")
    except User.DoesNotExist:
        logger.error(f"User {username} not found!")
        return None
    
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
    
    # Check for transaction issues
    reset_queries()
    
    # Create a knowledge entry with explicit transaction
    try:
        with transaction.atomic():
            # Create the entry
            entry = IndigenousKnowledge(
                title=title,
                description=description,
                practice_type="pest_control",
                materials=["Test material 1", "Test material 2"],
                crops=["Maize", "Beans"],
                pests=["Aphids", "Beetles"],
                seasons=["Summer", "Spring"],
                keeper=keeper,
                verification_status="pending",
                verification_count=0
            )
            
            # Save the entry
            entry.save()
            
            # Log the SQL queries
            for query in connection.queries:
                logger.info(f"SQL: {query['sql']}")
            
            logger.info(f"Created entry: ID {entry.id}, Title: {entry.title}")
            return entry
    except Exception as e:
        logger.error(f"Error creating entry: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def fix_form_issues():
    """Fix any issues with the form submission process."""
    # Check for database connection issues
    try:
        connection.ensure_connection()
        logger.info("Database connection is working")
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return
    
    # Check for transaction issues
    try:
        with transaction.atomic():
            # Test transaction
            pass
        logger.info("Transactions are working")
    except Exception as e:
        logger.error(f"Transaction error: {str(e)}")
        return
    
    # Check for permission issues
    try:
        # Create a test entry
        timestamp = int(time.time())
        title = f"Debug Form Test - {timestamp}"
        description = "This is a test entry created by the debug script"
        
        # Try for each user to find permission issues
        users = User.objects.all()
        for user in users:
            logger.info(f"Testing form submission for user: {user.username}")
            entry = simulate_form_submission(user.username, f"{title} - {user.username}", description)
            if entry:
                logger.info(f"Successfully created entry for {user.username}")
            else:
                logger.error(f"Failed to create entry for {user.username}")
    except Exception as e:
        logger.error(f"Permission error: {str(e)}")
        return

if __name__ == "__main__":
    logger.info("=== DEBUGGING FORM SUBMISSION ISSUES ===")
    fix_form_issues()
    
    logger.info("\n=== CHECKING FINAL DATABASE STATE ===")
    entries = IndigenousKnowledge.objects.all().order_by('-date_added')
    logger.info(f"Total knowledge entries: {entries.count()}")
    
    for entry in entries[:5]:  # Show only the 5 most recent entries
        logger.info(f"ID: {entry.id}, Title: {entry.title}, User: {entry.keeper.user.username}")
    
    logger.info("\nDebug script completed. Please check the logs for any issues.")
