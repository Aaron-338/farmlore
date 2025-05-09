#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
django.setup()

from django.contrib.auth.models import User

# Check if superuser exists
if not User.objects.filter(username='admin').exists():
    # Create a superuser
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully.')
else:
    print('Superuser already exists.') 