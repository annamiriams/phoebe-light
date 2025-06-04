from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """Custom User model with location fields"""
    # Django's built-in fields are inherited:
    # username, email, password, first_name, last_name, etc.
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Issue(models.Model):
    number = models.PositiveIntegerField(unique=True)
        # Maybe try to have this increment automatically but leaving as is for now.
    custom_title = models.CharField(max_length=100, blank=True)
        # Leaves room for 'Special Issue' or the like.
    editors_note = models.TextField(max_length=500)
    
    def __str__(self):
        return self.title
    
    @property
    def title(self):
        return self.custom_title or f'Issue {self.number}'
        # If a custom_title exists, use that as the title. Otherwise, use 'Issue 1', 'Issue 2', etc.
        # Property allows either a custom title or standardized issue title to be used. It's needed because title is based on logic (vs the return in the User model which isn't based on any logic.)
        
class Submission(models.Model):
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    title = models.CharField(max_length=500, blank=False)
    author = models.CharField(max_length=50, blank=False)
    author_bio = models.TextField(max_length=500, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_text = models.TextField(blank=False)
        # No set max_length at this point.
    approval_status = models.CharField(max_length=8, choices=APPROVAL_STATUS, default='pending')
    approved_issue = models.ForeignKey(Issue, null=True, blank=True, on_delete=models.SET_NULL)
        # on_delete is required, and I don't want to cascade delete here (if an issue is deleted, I want to keep all corresponding submissions). SET_NULL unlinks the issue and submission to keep the latter. 
    
    def __str__(self):
        return self.title