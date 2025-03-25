from django.db import models
from django.contrib.auth.models import User
from candidates.models import Candidate
from jobs.models import JobPost

class Note(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Note by {self.author.username} on {self.candidate}"

class Interview(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interviews')
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    interviewers = models.ManyToManyField(User, related_name='conducted_interviews')
    scheduled_at = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    location = models.CharField(max_length=200, blank=True, help_text="Physical location or virtual meeting link")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Interview with {self.candidate} for {self.job}"

class EmailTemplate(models.Model):
    TYPE_CHOICES = [
        ('application_received', 'Application Received'),
        ('interview_invitation', 'Interview Invitation'),
        ('rejection', 'Rejection'),
        ('offer', 'Job Offer'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name