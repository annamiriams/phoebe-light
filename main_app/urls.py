from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('submissions/', views.SubmissionCreate.as_view(), name='submissions'),
    path('submissions/<int:pk>/', views.SubmissionDetail.as_view(), name='submission-detail'),
    path('submissions/<int:pk>/update/', views.SubmissionUpdate.as_view(), name='submission-update'),
    path('submissions/<int:pk>/delete/', views.SubmissionDelete.as_view(), name='submission-delete'),
]