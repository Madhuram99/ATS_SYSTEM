# candidates/models.py
from django.db import models
from jobs.models import JobPost
import uuid
import os

def resume_file_path(instance, filename):
    # Generate a unique filename for uploaded resumes
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', filename)

class Candidate(models.Model):
    STAGE_CHOICES = [
        ('new', 'New'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('technical', 'Technical Assessment'),
        ('final', 'Final Interview'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to=resume_file_path)
    cover_letter = models.TextField(blank=True)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='candidates')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CandidateSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=100)
    years_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.skill} ({self.years_experience} years)"

class CandidateEducation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

class CandidateWorkExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='work_experience')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.position} at {self.company}"