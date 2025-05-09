"""
Management command to create user groups with appropriate permissions.

This command creates the following groups:
- knowledge_keeper: Can contribute indigenous knowledge
- community_member: Can validate knowledge and make observations
- knowledge_seeker: Can only access the chatbot (default for new users)
- administrator: Has full access to all features
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from community.models import IndigenousKnowledge, KnowledgeKeeper, RegionalObservation, CommunityValidation


class Command(BaseCommand):
    help = 'Creates user groups with appropriate permissions'

    def handle(self, *args, **options):
        # Create groups if they don't exist
        knowledge_keeper, created = Group.objects.get_or_create(name='knowledge_keeper')
        community_member, created = Group.objects.get_or_create(name='community_member')
        knowledge_seeker, created = Group.objects.get_or_create(name='knowledge_seeker')
        administrator, created = Group.objects.get_or_create(name='administrator')

        self.stdout.write(self.style.SUCCESS('User groups created successfully'))

        # Get content types for our models
        indigenous_knowledge_ct = ContentType.objects.get_for_model(IndigenousKnowledge)
        knowledge_keeper_ct = ContentType.objects.get_for_model(KnowledgeKeeper)
        regional_observation_ct = ContentType.objects.get_for_model(RegionalObservation)
        community_validation_ct = ContentType.objects.get_for_model(CommunityValidation)

        # Define permissions for knowledge keepers
        knowledge_keeper_perms = [
            # Can add/change/view their own indigenous knowledge
            Permission.objects.get(codename='add_indigenousknowledge', content_type=indigenous_knowledge_ct),
            Permission.objects.get(codename='change_indigenousknowledge', content_type=indigenous_knowledge_ct),
            Permission.objects.get(codename='view_indigenousknowledge', content_type=indigenous_knowledge_ct),
            # Can view other knowledge keepers
            Permission.objects.get(codename='view_knowledgekeeper', content_type=knowledge_keeper_ct),
            # Can add/view regional observations
            Permission.objects.get(codename='add_regionalobservation', content_type=regional_observation_ct),
            Permission.objects.get(codename='view_regionalobservation', content_type=regional_observation_ct),
            # Can validate knowledge
            Permission.objects.get(codename='add_communityvalidation', content_type=community_validation_ct),
            Permission.objects.get(codename='view_communityvalidation', content_type=community_validation_ct),
        ]

        # Define permissions for community members
        community_member_perms = [
            # Can view indigenous knowledge
            Permission.objects.get(codename='view_indigenousknowledge', content_type=indigenous_knowledge_ct),
            # Can view knowledge keepers
            Permission.objects.get(codename='view_knowledgekeeper', content_type=knowledge_keeper_ct),
            # Can add/view regional observations
            Permission.objects.get(codename='add_regionalobservation', content_type=regional_observation_ct),
            Permission.objects.get(codename='view_regionalobservation', content_type=regional_observation_ct),
            # Can validate knowledge
            Permission.objects.get(codename='add_communityvalidation', content_type=community_validation_ct),
            Permission.objects.get(codename='view_communityvalidation', content_type=community_validation_ct),
        ]

        # Knowledge seekers have no special permissions - they can only access the chatbot

        # Assign permissions to groups
        knowledge_keeper.permissions.set(knowledge_keeper_perms)
        community_member.permissions.set(community_member_perms)
        # No permissions for knowledge_seeker as they only access the chatbot
        # Administrator group has all permissions by default in the admin interface

        self.stdout.write(self.style.SUCCESS('Permissions assigned successfully'))
