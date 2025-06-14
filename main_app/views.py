from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from .models import Submission, Issue
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SubmissionForm
from django.urls import reverse_lazy

def home(request):
    issues = Issue.objects.prefetch_related('submissions').all().order_by('-number')
    
    return render(request, 'home.html', {
        'issues': issues,
    })

def about(request):
    return render(request, 'about.html')

class IssueDetail(DetailView):
    model = Issue
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = self.get_object()
        
        submissions_in_issue = issue.submissions.filter(approval_status = 'accepted')
        
        # Dictionary for unique authors in case they have multiple submissions (because a dictionary doesn't allow duplicate entries.)
        unique_authors={}
        for submission in submissions_in_issue:
            if submission.created_by_id not in unique_authors:
                unique_authors[submission.created_by_id] = submission.author
                
        context['authors'] = unique_authors
        return context

# TemplateView used because there is no direct model to pull from. Rather the view builds context from multiple queries 
class AuthorDetail(TemplateView):
    template_name = 'main_app/author_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # PKs from the URL:
        issue_pk = self.kwargs['issue_pk']
        author_pk = self.kwargs['author_pk']
        
        # Filter through submissions for all submissions that match the issue and author, and have accepted approval status.
        context['submissions'] = Submission.objects.filter(
            approved_issue_id = issue_pk,
            created_by_id = author_pk,
            approval_status = 'accepted'
        )
        
        # Find the Issue object and add it to the context.
        context['issue'] = Issue.objects.get(pk=issue_pk)
        
        # Find the first submission that matches the above context and add the author and author_bio to the context.  
        context['author_name'] = context['submissions'].first().author
        context['author_bio'] = context['submissions'].first().author_bio
            
        return context

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

class SubmissionDetail(LoginRequiredMixin, DetailView):
    model = Submission
    
class SubmissionUpdate(LoginRequiredMixin, UpdateView):
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
    
class SubmissionDelete(LoginRequiredMixin, DeleteView):
    model = Submission
    success_url = '/'