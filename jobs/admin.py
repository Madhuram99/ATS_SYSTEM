from django.contrib import admin
from .models import JobPost, Department

admin.site.register(JobPost)
admin.site.register(Department)  # If you want to manage departments too