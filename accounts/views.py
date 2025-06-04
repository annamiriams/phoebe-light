from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView

from .forms import RegisterUserForm
    # Used so we can customize the user registration form.

# Create your views here.

def signupView(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object that includes the data from the browser.
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = RegisterUserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'accounts/signup.html', context)

class Login(LoginView):
    template_name = 'accounts/login.html'
    
def logoutView(request):
    logout(request)
    return redirect ('home')