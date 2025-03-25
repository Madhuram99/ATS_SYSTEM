# recruiters/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Note, Interview, EmailTemplate
from candidates.models import Candidate
from jobs.models import JobPost
from django.utils import timezone

class NoteForm(forms.ModelForm):
    """
    Form for creating and editing recruiter notes about candidates
    """
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Enter your notes about this candidate...'
            }),
        }
        labels = {
            'content': 'Note',
        }

class InterviewForm(forms.ModelForm):
    """
    Form for scheduling interviews with candidates
    """
    interviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        required=True
    )
    
    # Add a minimum date validation for the scheduled_at field
    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text="Schedule date and time for the interview"
    )
    
    class Meta:
        model = Interview
        fields = ['interviewers', 'scheduled_at', 'duration', 'location', 'notes']
        widgets = {
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 15,
                'max': 240,
                'step': 15
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Office location or virtual meeting link'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Additional notes about this interview...'
            }),
        }
    
    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data.get('scheduled_at')
        if scheduled_at and scheduled_at < timezone.now():
            raise forms.ValidationError("Interview cannot be scheduled in the past.")
        return scheduled_at
    
    def clean(self):
        cleaned_data = super().clean()
        # You could add additional validation here
        # For example, check if interviewers are available at the scheduled time
        return cleaned_data

class EmailTemplateForm(forms.ModelForm):
    """
    Form for creating and editing email templates
    """
    class Meta:
        model = EmailTemplate
        fields = ['name', 'type', 'subject', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={
                'rows': 10, 
                'class': 'form-control',
                'placeholder': 'Enter email template content...\nYou can use variables like {{candidate.first_name}}, {{job.title}}, etc.'
            }),
        }

class SendEmailForm(forms.Form):
    """
    Form for sending emails to candidates
    """
    template = forms.ModelChoiceField(
        queryset=EmailTemplate.objects.all(),
        required=False,
        empty_label="Select a template (optional)",
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10, 
            'class': 'form-control',
            'placeholder': 'Enter email content...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        template_id = kwargs.pop('template_id', None)
        super(SendEmailForm, self).__init__(*args, **kwargs)
        
        if template_id:
            self.fields['template'].initial = template_id

class CandidateStageUpdateForm(forms.ModelForm):
    """
    Form for updating a candidate's recruitment stage
    """
    class Meta:
        model = Candidate
        fields = ['stage']
        widgets = {
            'stage': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super(CandidateStageUpdateForm, self).__init__(*args, **kwargs)
        self.fields['stage'].label = "Update recruitment stage"

class InterviewFeedbackForm(forms.Form):
    """
    Form for providing feedback after an interview
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    ]
    
    technical_skills = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'list-unstyled d-flex gap-3'})
    )
    communication = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'list-unstyled d-flex gap-3'})
    )
    culture_fit = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'list-unstyled d-flex gap-3'})
    )
    strengths = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'Candidate strengths...'
        })
    )
    weaknesses = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'Areas for improvement...'
        })
    )
    overall_comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4, 
            'class': 'form-control',
            'placeholder': 'Overall assessment and comments...'
        })
    )
    recommendation = forms.ChoiceField(
        choices=[
            ('hire', 'Hire'),
            ('consider', 'Consider for another round'),
            ('reject', 'Reject')
        ],
        widget=forms.RadioSelect(attrs={'class': 'list-unstyled'})
    )