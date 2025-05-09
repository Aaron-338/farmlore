#!/usr/bin/env python
"""
Script to monitor form submissions and database changes.
"""
import os
import django
import logging
import time
import json
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import IndigenousKnowledge, KnowledgeKeeper
from django.db.models.signals import post_save
from django.dispatch import receiver

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("form_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Record initial state
initial_entries = list(IndigenousKnowledge.objects.all().values('id', 'title', 'keeper__user__username', 'date_added'))
logger.info(f"Initial state: {len(initial_entries)} entries")
for entry in initial_entries:
    logger.info(f"ID: {entry['id']}, Title: {entry['title']}, User: {entry['keeper__user__username']}")

# Set up signal handler to monitor new entries
@receiver(post_save, sender=IndigenousKnowledge)
def log_knowledge_save(sender, instance, created, **kwargs):
    """Log when a knowledge entry is saved."""
    if created:
        logger.info(f"NEW ENTRY CREATED: ID: {instance.id}, Title: {instance.title}")
        logger.info(f"  Keeper: {instance.keeper}, User: {instance.keeper.user.username}")
        logger.info(f"  Date: {instance.date_added}")
        logger.info(f"  Materials: {json.dumps(instance.materials)}")
        logger.info(f"  Crops: {json.dumps(instance.crops)}")
        logger.info(f"  Pests: {json.dumps(instance.pests)}")
    else:
        logger.info(f"ENTRY UPDATED: ID: {instance.id}, Title: {instance.title}")

# Connect the signal
post_save.connect(log_knowledge_save, sender=IndigenousKnowledge)

logger.info("Monitoring started. Watching for new knowledge entries...")
logger.info("Press Ctrl+C to stop monitoring.")

# Keep script running
try:
    while True:
        time.sleep(5)
        current_count = IndigenousKnowledge.objects.count()
        if current_count > len(initial_entries):
            new_entries = IndigenousKnowledge.objects.exclude(id__in=[e['id'] for e in initial_entries])
            logger.info(f"Found {new_entries.count()} new entries since script started")
            for entry in new_entries:
                logger.info(f"New entry: ID: {entry.id}, Title: {entry.title}, User: {entry.keeper.user.username}")
            # Update initial entries
            initial_entries = list(IndigenousKnowledge.objects.all().values('id', 'title', 'keeper__user__username', 'date_added'))
except KeyboardInterrupt:
    logger.info("Monitoring stopped.")
