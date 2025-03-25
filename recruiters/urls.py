from django.urls import path
from . import views

urlpatterns = [
    path('notes/add/<int:candidate_id>/', views.add_note, name='add_note'),
    path('interviews/schedule/<int:candidate_id>/<int:job_id>/', views.schedule_interview, name='schedule_interview'),
    path('email/<int:candidate_id>/', views.send_email, name='send_email'),
    path('email/<int:candidate_id>/<int:template_id>/', views.send_email, name='send_email_with_template'),
]