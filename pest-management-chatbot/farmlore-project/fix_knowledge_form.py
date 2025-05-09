#!/usr/bin/env python
"""
Script to fix knowledge form submission and visibility issues.
"""
import os
import django
import logging
import json
import time
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from community.models import IndigenousKnowledge, KnowledgeKeeper
from django.db import transaction

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def list_all_entries():
    """List all knowledge entries in the database."""
    entries = IndigenousKnowledge.objects.all().order_by('-date_added')
    logger.info(f"Total knowledge entries: {entries.count()}")
    
    for entry in entries:
        logger.info(f"ID: {entry.id}, Title: {entry.title}, Status: {entry.verification_status}")
        logger.info(f"  Keeper: {entry.keeper}, User: {entry.keeper.user.username}")
        logger.info(f"  Date Added: {entry.date_added}")
        logger.info("---")

def fix_form_submission():
    """Fix issues with knowledge form submission."""
    # Check if there are any entries with empty or null keeper
    broken_entries = IndigenousKnowledge.objects.filter(keeper__isnull=True)
    logger.info(f"Found {broken_entries.count()} entries with null keeper")
    
    for entry in broken_entries:
        logger.info(f"Fixing entry: {entry.id} - {entry.title}")
        # Assign to admin user as a fallback
        admin = User.objects.get(username='admin')
        try:
            keeper = admin.knowledge_keeper
        except KnowledgeKeeper.DoesNotExist:
            keeper = KnowledgeKeeper.objects.create(
                user=admin,
                village='Admin Village',
                district='Admin District',
                years_experience=10
            )
        
        entry.keeper = keeper
        entry.save()
        logger.info(f"  Fixed - now assigned to keeper: {entry.keeper}")

def create_test_entry_for_all_users():
    """Create a test entry for all users to verify visibility."""
    users = User.objects.all()
    logger.info(f"Creating test entries for {users.count()} users")
    
    for user in users:
        logger.info(f"Creating entry for user: {user.username}")
        try:
            # Get or create keeper
            try:
                keeper = user.knowledge_keeper
            except KnowledgeKeeper.DoesNotExist:
                keeper = KnowledgeKeeper.objects.create(
                    user=user,
                    village=f"{user.username}'s Village",
                    district='Test District',
                    years_experience=5
                )
            
            # Create entry with transaction to ensure it's fully committed
            with transaction.atomic():
                timestamp = int(time.time())
                entry = IndigenousKnowledge.objects.create(
                    title=f"Test Entry by {user.username} at {datetime.now().strftime('%H:%M:%S')}",
                    description=f"This is a test entry created by {user.username} to verify visibility.",
                    practice_type="pest_control",
                    materials=["Test material 1", "Test material 2"],
                    crops=["Maize", "Beans"],
                    pests=["Aphids", "Beetles"],
                    seasons=["Summer", "Spring"],
                    keeper=keeper,
                    verification_status="pending",
                    verification_count=0
                )
                
                # Force a save to ensure it's committed
                entry.save()
                
                logger.info(f"  Created entry: {entry.id} - {entry.title}")
                logger.info(f"  Keeper: {entry.keeper}, User: {user.username}")
        except Exception as e:
            logger.error(f"Error creating entry for {user.username}: {str(e)}")

def fix_dashboard_view():
    """Fix the dashboard view to ensure all entries are visible."""
    # This is a placeholder for manual fixes to the dashboard view
    logger.info("To fix the dashboard view:")
    logger.info("1. Ensure CommunityDashboardView.get_queryset() doesn't filter entries")
    logger.info("2. Check for any caching issues in the template")
    logger.info("3. Verify that the template is displaying all entries correctly")

if __name__ == "__main__":
    logger.info("=== CHECKING ALL KNOWLEDGE ENTRIES ===")
    list_all_entries()
    
    logger.info("\n=== FIXING FORM SUBMISSION ISSUES ===")
    fix_form_submission()
    
    logger.info("\n=== CREATING TEST ENTRIES FOR ALL USERS ===")
    create_test_entry_for_all_users()
    
    logger.info("\n=== FINAL CHECK OF ALL ENTRIES ===")
    list_all_entries()
    
    logger.info("\n=== DASHBOARD VIEW RECOMMENDATIONS ===")
    fix_dashboard_view()
    
    logger.info("\nScript completed. Please restart the web server and check the dashboard.")
