"""
Test script to directly add a knowledge entry to the database.
Run this script with: python test_knowledge.py
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pest_management.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from community.models import KnowledgeKeeper, IndigenousKnowledge

def create_test_knowledge():
    """Create a test knowledge entry."""
    print("Creating test knowledge entry...")
    
    # Get or create a test user
    try:
        user = User.objects.get(username='testuser')
        print(f"Using existing user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        print(f"Created new user: {user.username}")
    
    # Get or create a knowledge keeper
    try:
        keeper = KnowledgeKeeper.objects.get(user=user)
        print(f"Using existing keeper: {keeper}")
    except KnowledgeKeeper.DoesNotExist:
        keeper = KnowledgeKeeper.objects.create(
            user=user,
            village='Test Village',
            district='Test District',
            years_experience=10
        )
        print(f"Created new keeper: {keeper}")
    
    # Create a knowledge entry
    knowledge = IndigenousKnowledge.objects.create(
        title='Test Knowledge Entry',
        description='This is a test knowledge entry created by the test script.',
        practice_type='pest_control',
        materials=['Ash', 'Water', 'Soap'],
        crops=['Maize', 'Beans'],
        pests=['Aphids', 'Beetles'],
        seasons=['summer', 'spring'],
        keeper=keeper
    )
    
    print(f"Created knowledge entry: {knowledge.title} (ID: {knowledge.id})")
    print(f"Verification status: {knowledge.verification_status}")
    print(f"Materials: {knowledge.materials}")
    print(f"Crops: {knowledge.crops}")
    print(f"Pests: {knowledge.pests}")
    print(f"Seasons: {knowledge.seasons}")
    
    # List all knowledge entries
    print("\nAll knowledge entries in the database:")
    for entry in IndigenousKnowledge.objects.all().order_by('-date_added'):
        print(f"- {entry.title} (ID: {entry.id}, Status: {entry.verification_status})")

if __name__ == '__main__':
    create_test_knowledge()
