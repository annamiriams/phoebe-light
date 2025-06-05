from django import forms
from .models import Submission, Issue
from accounts.models import User

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title',
            'author',
            'submission_text',
            'author_bio',
        ]