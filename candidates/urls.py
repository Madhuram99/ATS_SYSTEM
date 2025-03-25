# candidates/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_list, name='candidate_list'),
    path('<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
    path('create/', views.candidate_create, name='candidate_create'),
    path('create/<int:job_id>/', views.candidate_create, name='candidate_create_for_job'),
    path('<int:candidate_id>/parse-resume/', views.parse_resume, name='parse_resume'),
    path('<int:candidate_id>/update-stage/', views.update_stage, name='update_stage'),
    
    # Add these new URL patterns
    path('<int:candidate_id>/add-skill/', views.add_skill, name='add_skill'),
    path('<int:skill_id>/edit-skill/', views.edit_skill, name='edit_skill'),
    path('<int:candidate_id>/add-education/', views.add_education, name='add_education'),
    path('<int:education_id>/edit-education/', views.edit_education, name='edit_education'),
    path('<int:candidate_id>/add-experience/', views.add_experience, name='add_experience'),
    path('<int:experience_id>/edit-experience/', views.edit_experience, name='edit_experience'),
    path('<int:candidate_id>/add-note/', views.add_note, name='add_note'),
    path('<int:candidate_id>/send-email/', views.send_email, name='send_email'),
]