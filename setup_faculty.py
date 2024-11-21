import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Attendence_System.settings')
django.setup()

from django.contrib.auth.models import User
from attendence_sys.models import Faculty

# Get the superuser we created
user = User.objects.get(username='Om')

# Create faculty profile for the user
faculty = Faculty.objects.create(
    user=user,
    firstname='Om',
    lastname='Faculty',
    phone='1234567890',
    email=user.email
)

print("Faculty profile created successfully!")
