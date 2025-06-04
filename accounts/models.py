from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User model with location fields"""
    # Django's built-in fields are inherited:
    # username, email, password, first_name, last_name, etc.
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    