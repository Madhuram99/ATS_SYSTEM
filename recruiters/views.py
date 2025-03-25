# recruiters/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Template, Context
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Note, Interview, EmailTemplate
from .forms import (
    NoteForm, InterviewForm, EmailTemplateForm, SendEmailForm,
    CandidateStageUpdateForm, InterviewFeedbackForm
)
from candidates.models import Candidate
from jobs.models import JobPost

@login_required
def add_note(request, candidate_id):
    """
    Add a note to a candidate's profile
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.candidate = candidate
            note.author = request.user
            note.save()
            messages.success(request, 'Note added successfully!')
            return redirect('candidate_detail', candidate_id=candidate.id)
    else:
        form = NoteForm()
    
    return render(request, 'recruiters/note_form.html', {
        'form': form,
        'candidate': candidate
    })

@login_required
def schedule_interview(request, candidate_id, job_id):
    """
    Schedule an interview with a candidate
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    job = get_object_or_404(JobPost, id=job_id)
    
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.candidate = candidate
            interview.job = job
            interview.save()
            
            # Save many-to-many relationships
            form.save_m2m()
            
            messages.success(request, f'Interview with {candidate.first_name} {candidate.last_name} scheduled successfully!')
            
            # Update candidate stage if it's still in early stages
            if candidate.stage in ['new', 'screening']:
                candidate.stage = 'interview'
                candidate.save()
            
            # In a real implementation, this would send email notifications
            # notify_candidate_and_interviewers(interview)
            
            return redirect('candidate_detail', candidate_id=candidate.id)
    else:
        form = InterviewForm()
    
    return render(request, 'recruiters/interview_form.html', {
        'form': form,
        'candidate': candidate,
        'job': job
    })

@login_required
def email_template_list(request):
    """
    List all email templates
    """
    templates = EmailTemplate.objects.all().order_by('type', 'name')
    return render(request, 'recruiters/email_template_list.html', {
        'templates': templates
    })

@login_required
def email_template_create(request):
    """
    Create a new email template
    """
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            messages.success(request, 'Email template created successfully!')
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm()
    
    return render(request, 'recruiters/email_template_form.html', {
        'form': form,
        'title': 'Create Email Template'
    })
    
@login_required
def send_email(request, candidate_id):
    """
    Send an email to a candidate using a selected template
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            template = form.cleaned_data['template']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            # If a template is selected, render its body
            if template:
                body = Template(template.body).render(Context({
                    'candidate': candidate,
                    'job': candidate.job,
                    'recruiter': request.user
                }))
            
            # Send the email
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [candidate.email],
                fail_silently=False,
            )
            
            # Show a success message
            messages.success(request, f'Email sent to {candidate.first_name} {candidate.last_name}!')
            return redirect('candidate_detail', candidate_id=candidate.id)
    else:
        form = SendEmailForm()
    
    return render(request, 'recruiters/send_email_form.html', {
        'form': form,
        'candidate': candidate
    })    