"""
Create superuser for the corpus platform
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_compilation.settings')
django.setup()

from accounts.models import CustomUser

# Create superuser if it doesn't exist
if not CustomUser.objects.filter(username='admin').exists():
    user = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@corpus.gov.tr',
        password='admin123',
        role=CustomUser.Role.ADMIN,
        is_approved=True
    )
    print(f'Superuser created successfully!')
    print(f'Username: admin')
    print(f'Password: admin123')
    print(f'Email: admin@corpus.gov.tr')
else:
    print('Superuser already exists!')
