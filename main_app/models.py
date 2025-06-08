from django.db import models
from django.conf import settings
    # Updating per refactoring of User model to accounts/models.py.
from django_ckeditor_5.fields import CKEditor5Field

class Issue(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    number = models.PositiveIntegerField(unique=True)
        # Maybe try to have this increment automatically but leaving as is for now.
    custom_title = models.CharField(max_length=100, blank=True)
        # Leaves room for 'Special Issue' or the like.
    editors_note = CKEditor5Field()
    published_authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='published_issues')
        # related_name will let me reverse search (find a user's published_issues on an author's page)
    status = models.CharField(max_length=9, choices=STATUS, default='pending')
    
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
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    title = models.CharField(max_length=500, blank=False)
    author = models.CharField(max_length=100, blank=False)
    author_bio = CKEditor5Field()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        # Updating per refactoring of User model to accounts/models.py.
    submission_text = CKEditor5Field()
        # No set max_length at this point.
    approval_status = models.CharField(max_length=8, choices=APPROVAL_STATUS, default='pending')
    approved_issue = models.ForeignKey(Issue, null=True, blank=True, on_delete=models.SET_NULL, related_name='submissions')
        # on_delete is required, and I don't want to cascade delete here (if an issue is deleted, I want to keep all corresponding submissions). SET_NULL unlinks the issue and submission to keep the latter. 
        # adding related_name so I can reverse search on the model
         
    def __str__(self):
        return self.title