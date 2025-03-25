# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:job_id>/edit/', views.job_edit, name='job_edit'),
]