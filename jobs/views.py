# jobs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPost, Department
from .forms import JobPostForm

@login_required
def job_list(request):
    jobs = JobPost.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    candidates = job.candidates.all().order_by('-created_at')
    return render(request, 'jobs/job_detail.html', {'job': job, 'candidates': candidates})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Job post created successfully!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobPostForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Create Job Post'})

@login_required
def job_edit(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobPostForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job Post'})