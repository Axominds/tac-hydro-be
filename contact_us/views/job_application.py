from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from contact_us.models import JobApplication
from contact_us.serializers.job_application import (
    JobApplicationCreateSerializer,
    JobApplicationDetailSerializer,
    JobApplicationListSerializer,
    JobApplicationUpdateSerializer,
)
from home.models import SiteSettings
import logging

logger = logging.getLogger(__name__)

from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class JobApplicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationDetailSerializer
    pagination_class = JobApplicationPagination
    list_serializer_class = JobApplicationListSerializer
    create_serializer_class = JobApplicationCreateSerializer
    update_serializer_class = JobApplicationUpdateSerializer
    partial_update_serializer_class = JobApplicationUpdateSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action == "create":
            return self.create_serializer_class
        if self.action in ["update", "partial_update"]:
            return self.update_serializer_class
        return super().get_serializer_class()

    def paginate_queryset(self, queryset):
        if "page" not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        qs = JobApplication.objects.all().order_by("-submitted_at")
        
        job_id = self.request.query_params.get("job_id")
        if job_id:
            qs = qs.filter(job_id=job_id)
            
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
            
        return qs

    def perform_create(self, serializer):
        application = serializer.save()
        
        try:
            site_settings = SiteSettings.objects.first()
            to_email = site_settings.contact_email if site_settings else None

            if to_email:
                applicant_name = f"{application.first_name} {application.last_name}".strip()
                job_title = application.job.title if application.job else "Unknown Job"
                subject = f"New Job Application: {job_title} from {applicant_name}"

                context = {
                    "applicant_name": applicant_name,
                    "job_title": job_title,
                    "email": application.email,
                    "phone": application.phone,
                    "degree": application.degree,
                    "college": application.college,
                    "contact_email": to_email,
                }

                html_content = render_to_string("job_application.html", context)
                text_content = f"""
New Job Application Received

Applicant: {applicant_name}
Job Title: {job_title}
Email: {application.email}
Phone: {application.phone}
Degree: {application.degree}
College: {application.college}

Please check the admin panel for more details and to download the CV/Cover Letter.
"""

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[to_email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
        except Exception as e:
            logger.error(f"Failed to send job application email: {e}")
