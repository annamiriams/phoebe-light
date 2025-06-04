from django.contrib import admin
from .models import Submission, Issue

# Register your models here.

admin.site.register(Submission)
admin.site.register(Issue)