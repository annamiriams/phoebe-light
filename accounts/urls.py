from django.urls import path, include
from . import views

urlpatterns = [
    # Sign up
    path('signup/', views.signupView, name='signup'),
    # Log in
    # path('login/', views.loginView, name='login'),
    # Log out
    # path('logout/', views.logoutView, name='logout'),
]