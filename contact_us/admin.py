from django.contrib import admin
from .models import JobPosting, JobApplication


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "location", "is_open", "published_at"]
    list_filter = ["is_open", "type"]
    search_fields = ["title"]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "job", "email", "submitted_at", "status"]
    list_filter = ["status", "job"]
    search_fields = ["first_name", "last_name", "email"]
