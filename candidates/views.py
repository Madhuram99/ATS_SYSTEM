from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate, CandidateSkill, CandidateEducation, CandidateWorkExperience
from .forms import CandidateForm, CandidateSkillFormSet, CandidateEducationFormSet, CandidateWorkExperienceFormSet
from jobs.models import JobPost
import pandas as pd
import re
from recruiters.forms import NoteForm 

@login_required
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('-created_at')
    return render(request, 'candidates/candidate_list.html', {'candidates': candidates})

@login_required
@login_required
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(
        Candidate.objects.prefetch_related(
            'interviews__interviewers',
            'skills',
            'education',
            'work_experience',
            'notes'
        ), 
        id=candidate_id
    )
    stages = ['new', 'screening', 'interview', 'technical', 'final', 'offer', 'hired', 'rejected']
    return render(request, 'candidates/candidate_detail.html', {
        'candidate': candidate,
        'stages': stages
    })
@login_required
def candidate_create(request, job_id=None):
    job = None
    if job_id:
        job = get_object_or_404(JobPost, id=job_id)
    
    # Get all published jobs for the dropdown
    jobs = JobPost.objects.filter(status='published').order_by('-created_at')
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, initial={'job': job})
        skill_formset = CandidateSkillFormSet(request.POST, prefix='skills')
        education_formset = CandidateEducationFormSet(request.POST, prefix='education')
        experience_formset = CandidateWorkExperienceFormSet(request.POST, prefix='experience')
        
        if form.is_valid() and skill_formset.is_valid() and education_formset.is_valid() and experience_formset.is_valid():
            candidate = form.save()
            
            # Save skills
            skills = skill_formset.save(commit=False)
            for skill in skills:
                skill.candidate = candidate
                skill.save()
            
            # Save education
            educations = education_formset.save(commit=False)
            for education in educations:
                education.candidate = candidate
                education.save()
            
            # Save work experience
            experiences = experience_formset.save(commit=False)
            for experience in experiences:
                experience.candidate = candidate
                experience.save()
            
            messages.success(request, 'Candidate added successfully!')
            return redirect('candidate_detail', candidate_id=candidate.id)
    else:
        form = CandidateForm(initial={'job': job})
        skill_formset = CandidateSkillFormSet(prefix='skills')
        education_formset = CandidateEducationFormSet(prefix='education')
        experience_formset = CandidateWorkExperienceFormSet(prefix='experience')
    
    return render(request, 'candidates/candidate_form.html', {
        'form': form,
        'skill_formset': skill_formset,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'job': job,
        'jobs': jobs  # Add this line to pass jobs to the template
    })

@login_required
def parse_resume(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    # In a real implementation, this would use a resume parsing library or API
    # For demonstration, we'll just simulate parsing with some basic logic
    
    # Read the resume file (assuming text or PDF that can be converted to text)
    resume_text = "Sample resume text extracted from file"
    
    # Extract skills (simplified logic)
    skills = ['Python', 'Django', 'JavaScript']
    for skill in skills:
        CandidateSkill.objects.create(
            candidate=candidate,
            skill=skill,
            years_experience=1  # Default value
        )
    
    messages.success(request, 'Resume parsed successfully!')
    return redirect('candidate_detail', candidate_id=candidate.id)

@login_required
def update_stage(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        new_stage = request.POST.get('stage')
        candidate.stage = new_stage
        candidate.save()
        messages.success(request, f'Stage updated to {candidate.get_stage_display()}')
    return redirect('candidate_detail', candidate_id=candidate.id)

@login_required
def add_skill(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        skill = request.POST.get('skill')
        years = request.POST.get('years_experience', 0)
        if skill:
            CandidateSkill.objects.create(
                candidate=candidate,
                skill=skill,
                years_experience=years
            )
            messages.success(request, 'Skill added successfully!')
        return redirect('candidate_detail', candidate_id=candidate.id)
    return render(request, 'candidates/add_skill.html', {'candidate': candidate})

@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(CandidateSkill, id=skill_id)
    if request.method == 'POST':
        skill.skill = request.POST.get('skill')
        skill.years_experience = request.POST.get('years_experience', 0)
        skill.save()
        messages.success(request, 'Skill updated successfully!')
        return redirect('candidate_detail', candidate_id=skill.candidate.id)
    return render(request, 'candidates/edit_skill.html', {'skill': skill})

# Similar implementations for education and experience views
@login_required
def add_education(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    # Implementation similar to add_skill
    pass

@login_required
def edit_education(request, education_id):
    education = get_object_or_404(CandidateEducation, id=education_id)
    # Implementation similar to edit_skill
    pass

@login_required
def add_experience(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    # Implementation similar to add_skill
    pass

@login_required
def edit_experience(request, experience_id):
    experience = get_object_or_404(CandidateWorkExperience, id=experience_id)
    # Implementation similar to edit_skill
    pass

@login_required
def send_email(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    # Implementation for sending email
    pass

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