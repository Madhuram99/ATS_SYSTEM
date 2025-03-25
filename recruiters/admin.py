from django.contrib import admin
from .models import Note, Interview, EmailTemplate

class NoteAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'author', 'created_at', 'short_content')
    list_filter = ('author', 'created_at')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'content')
    raw_id_fields = ('candidate', 'author')
    date_hierarchy = 'created_at'

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'

class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'scheduled_at', 'duration', 'status')
    list_filter = ('status', 'job', 'scheduled_at')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'job__title')
    filter_horizontal = ('interviewers',)
    raw_id_fields = ('candidate', 'job')
    date_hierarchy = 'scheduled_at'
    fieldsets = (
        (None, {
            'fields': ('candidate', 'job', 'status')
        }),
        ('Interview Details', {
            'fields': ('scheduled_at', 'duration', 'location', 'interviewers')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_by', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'subject', 'body')
    raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'created_by')
        }),
        ('Content', {
            'fields': ('subject', 'body')
        }),
    )

admin.site.register(Note, NoteAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)