# candidates/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Candidate, CandidateSkill, CandidateEducation, CandidateWorkExperience

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'email', 'phone', 'resume', 'cover_letter', 'job', 'stage']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }

CandidateSkillFormSet = inlineformset_factory(
    Candidate, CandidateSkill, 
    fields=['skill', 'years_experience'],
    extra=3, can_delete=True
)

CandidateEducationFormSet = inlineformset_factory(
    Candidate, CandidateEducation,
    fields=['institution', 'degree', 'field_of_study', 'from_date', 'to_date'],
    extra=2, can_delete=True
)

CandidateWorkExperienceFormSet = inlineformset_factory(
    Candidate, CandidateWorkExperience,
    fields=['company', 'position', 'from_date', 'to_date', 'description'],
    extra=2, can_delete=True
)