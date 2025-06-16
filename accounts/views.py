from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView

from .forms import RegisterUserForm

def registerView(request):
    error_message = ''
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = RegisterUserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'accounts/register.html', context)

class Login(LoginView):
    template_name = 'accounts/login.html'
    
def logoutView(request):
    logout(request)
    return redirect ('home')