from django.contrib import admin
from .models import Candidate, CandidateSkill, CandidateEducation, CandidateWorkExperience

class CandidateSkillInline(admin.TabularInline):
    model = CandidateSkill
    extra = 1

class CandidateEducationInline(admin.TabularInline):
    model = CandidateEducation
    extra = 1

class CandidateWorkExperienceInline(admin.TabularInline):
    model = CandidateWorkExperience
    extra = 1

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'job', 'stage', 'created_at')
    list_filter = ('stage', 'job', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'job__title')
    inlines = [CandidateSkillInline, CandidateEducationInline, CandidateWorkExperienceInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Application Details', {
            'fields': ('job', 'stage', 'resume', 'cover_letter')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'skill', 'years_experience')
    list_filter = ('skill',)
    search_fields = ('candidate__first_name', 'candidate__last_name', 'skill')

@admin.register(CandidateEducation)
class CandidateEducationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'degree', 'institution', 'field_of_study', 'from_date', 'to_date')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'institution', 'degree')

@admin.register(CandidateWorkExperience)
class CandidateWorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'position', 'company', 'from_date', 'to_date')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'company', 'position')
    list_filter = ('company',)