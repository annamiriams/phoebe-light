from django.shortcuts import render
from django.views.generic import CreateView
from .models import Submission, Issue
from .forms import SubmissionForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class SubmissionCreate(CreateView):
    model = Submission
    form_class = SubmissionForm
    success_url = '/submissions/'
        # Change to that submission show page.
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    # Pass a context variable to the SubmissionCreate view so that I can render a user's submissions on the page.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['submissions'] = Submission.objects.filter(created_by=self.request.user)
        else: 
            context['submissions'] = None
        return context