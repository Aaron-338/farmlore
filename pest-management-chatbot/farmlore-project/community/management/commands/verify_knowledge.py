from django.core.management.base import BaseCommand
from django.utils import timezone
from community.models import IndigenousKnowledge, CommunityValidation
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Force a knowledge entry to be verified by setting its verification count to 5'

    def add_arguments(self, parser):
        parser.add_argument('knowledge_id', type=int, help='ID of the knowledge entry to verify')

    def handle(self, *args, **options):
        knowledge_id = options['knowledge_id']
        
        try:
            # Get the knowledge entry
            knowledge = IndigenousKnowledge.objects.get(pk=knowledge_id)
            
            # Get existing validations
            current_validations = knowledge.validations.count()
            needed_validations = 5 - current_validations
            
            if needed_validations > 0:
                # Create the needed validations with different users
                for i in range(needed_validations):
                    # Create a unique username for each validation
                    username = f'system_validator_{i+1}'
                    
                    # Get or create a user for this validation
                    validator, created = User.objects.get_or_create(
                        username=username,
                        defaults={
                            'email': f'system{i+1}@farmlore.org', 
                            'is_staff': False,
                            'first_name': f'Validator',
                            'last_name': f'{i+1}'
                        }
                    )
                    
                    # Create the validation
                    CommunityValidation.objects.create(
                        knowledge=knowledge,
                        validator=validator,
                        rating=5,
                        comments=f'System validation #{i+1}',
                        has_used=True,
                        date_added=timezone.now()
                    )
            
            # Update the knowledge entry's verification status and count
            knowledge.verification_status = 'verified'
            knowledge.verification_count = 5
            knowledge.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully verified knowledge entry "{knowledge.title}" (ID: {knowledge_id})'))
            self.stdout.write(f'Verification count: {knowledge.verification_count}')
            self.stdout.write(f'Verification status: {knowledge.get_verification_status_display()}')
            
        except IndigenousKnowledge.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Knowledge entry with ID {knowledge_id} does not exist'))
