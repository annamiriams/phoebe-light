from django.urls import path, include
from . import views

urlpatterns = [
    # Sign up
    path('signup/', views.signupView, name='signup'),
    # Log in
    path('login/', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
        # Necessary to add template_name= to override the default login view at registration/login.html
    # Log out
    path('logout/', views.logoutView, name='logout'),
]