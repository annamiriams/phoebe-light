from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Submission, Issue
from django.contrib.auth.models import User
from .forms import SubmissionForm
from django.urls import reverse_lazy

def home(request):
    issues = Issue.objects.prefetch_related('submissions').all()
    
    return render(request, 'home.html', {
        'issues': issues,
    })

def about(request):
    return render(request, 'about.html')

class IssueDetail(DetailView):
    model = Issue

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

class SubmissionDetail(DetailView):
    model = Submission
    
class SubmissionUpdate(UpdateView):
    model = Submission
    fields = [
        'title',
        'author',
        'submission_text',
        'author_bio',
    ]
    
    # Return to details page using reverse_lazy, which doesn't generate the URL immediately.
    def get_success_url(self):
        return reverse_lazy('submission-detail', kwargs={'pk': self.object.pk})
    
    # Pass a context variable to SubmissionUpdate view so that I can remove user submissions from the update page.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
class SubmissionDelete(DeleteView):
    model = Submission
    success_url = '/'