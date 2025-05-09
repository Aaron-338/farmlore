#!/usr/bin/env python
"""
Real-time form submission tracker for FarmLore.

This script monitors form submissions in real-time and logs detailed information
about each submission attempt, successful or failed.
"""
import os
import django
import logging
import time
import json
import sys
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import IndigenousKnowledge, KnowledgeKeeper
from django.db import connection
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("form_tracker.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Track initial state
initial_entries = list(IndigenousKnowledge.objects.all().values_list('id', flat=True))
logger.info(f"Starting form tracker. Current entries in database: {len(initial_entries)}")
logger.info(f"Entry IDs: {initial_entries}")

# Set up signal handlers to track form submissions
@receiver(pre_save, sender=IndigenousKnowledge)
def track_pre_save(sender, instance, **kwargs):
    """Track pre-save events for IndigenousKnowledge."""
    is_new = instance.pk is None
    
    if is_new:
        logger.info(f"NEW ENTRY BEING CREATED: {instance.title}")
        logger.info(f"Keeper: {instance.keeper} (User: {instance.keeper.user.username if instance.keeper else 'None'})")
    else:
        logger.info(f"UPDATING EXISTING ENTRY: {instance.title} (ID: {instance.pk})")
    
    logger.info(f"Data: Title={instance.title}, Type={instance.practice_type}")
    logger.info(f"Materials: {instance.materials}")
    logger.info(f"Crops: {instance.crops}")
    logger.info(f"Pests: {instance.pests}")
    logger.info(f"Seasons: {instance.seasons}")
    logger.info(f"Verification Status: {instance.verification_status}")

@receiver(post_save, sender=IndigenousKnowledge)
def track_post_save(sender, instance, created, **kwargs):
    """Track post-save events for IndigenousKnowledge."""
    if created:
        logger.info(f"SUCCESS: Created new entry ID: {instance.pk}, Title: {instance.title}")
        logger.info(f"Keeper: {instance.keeper} (User: {instance.keeper.user.username if instance.keeper else 'None'})")
    else:
        logger.info(f"SUCCESS: Updated entry ID: {instance.pk}, Title: {instance.title}")
    
    # Check database state
    current_entries = list(IndigenousKnowledge.objects.all().order_by('-date_added')[:5].values('id', 'title', 'keeper__user__username'))
    logger.info(f"Current entries (showing latest 5):")
    for entry in current_entries:
        logger.info(f"ID: {entry['id']}, Title: {entry['title']}, User: {entry['keeper__user__username']}")

def monitor_entries():
    """Monitor for new entries continuously."""
    logger.info("Starting continuous monitoring for new entries...")
    
    last_check = datetime.now()
    check_interval = 5  # seconds
    
    try:
        while True:
            time.sleep(check_interval)
            
            # Check for new entries
            now = datetime.now()
            new_entries = IndigenousKnowledge.objects.filter(
                date_added__gt=last_check
            ).order_by('-date_added')
            
            if new_entries.exists():
                logger.info(f"Found {new_entries.count()} new entries since last check!")
                for entry in new_entries:
                    logger.info(f"New entry: ID={entry.id}, Title={entry.title}, User={entry.keeper.user.username if entry.keeper else 'None'}")
            
            last_check = now
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")

if __name__ == "__main__":
    logger.info("=== FORM SUBMISSION TRACKER STARTED ===")
    logger.info("This script will monitor all form submissions in real-time.")
    logger.info("Press Ctrl+C to stop monitoring.")
    logger.info("")
    
    # Start monitoring
    monitor_entries()
