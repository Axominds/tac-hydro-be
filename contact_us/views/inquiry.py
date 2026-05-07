from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from home.models import SiteSettings
from projects.models import ProjectScope
from contact_us.serializers.inquiry import (
    ContactInquirySerializer,
    CollaborationInquirySerializer,
)


class ContactInquiryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactInquirySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        site_settings = SiteSettings.objects.first()
        to_email = site_settings.contact_email if site_settings else None

        if not to_email:
            return Response(
                {"error": "Contact email not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        subject = f"New Contact Inquiry from {data.get('name', 'Unknown')}"

        project_scope_id = data.get("project_scope_id")
        project_scope_name = ""
        if project_scope_id:
            try:
                project_scope = ProjectScope.objects.get(id=project_scope_id)
                project_scope_name = project_scope.name
            except ProjectScope.DoesNotExist:
                pass

        context = {
            "name": data.get("name", ""),
            "phone": data.get("phone", ""),
            "email": data.get("email", ""),
            "project_scope_id": project_scope_name,
            "message": data.get("message", ""),
            "contact_email": to_email,
        }

        html_content = render_to_string("contact_inquiry.html", context)
        text_content = f"""
New Contact Inquiry

Name: {data.get('name', '')}
Phone: {data.get('phone', '')}
Email: {data.get('email', '')}
Project Scope ID: {data.get('project_scope_id')}
Message: {data.get('message', '')}
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return Response({"message": "Inquiry sent successfully"}, status=status.HTTP_200_OK)


class CollaborationInquiryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CollaborationInquirySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        site_settings = SiteSettings.objects.first()
        to_email = site_settings.collaboration_email if site_settings else None

        if not to_email:
            return Response(
                {"error": "Collaboration email not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        subject = f"New Collaboration Inquiry from {data.get('rep_name', 'Unknown')}"

        context = {
            "rep_name": data.get("rep_name", ""),
            "organization": data.get("organization", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "website": data.get("website", ""),
            "collab_type": data.get("collab_type", ""),
            "company_profile": data.get("company_profile", ""),
            "proposal_brief": data.get("proposal_brief", ""),
            "attachment": data.get("attachment"),
            "contact_email": to_email,
        }

        html_content = render_to_string("collaboration_inquiry.html", context)
        text_content = f"""
New Collaboration Inquiry

Representative Name: {data.get('rep_name', '')}
Organization: {data.get('organization', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
Website: {data.get('website', '')}
Collaboration Type: {data.get('collab_type', '')}
Company Profile: {data.get('company_profile', '')}
Proposal Brief: {data.get('proposal_brief', '')}
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_content, "text/html")

        attachment = data.get("attachment")
        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        email.send(fail_silently=False)

        return Response({"message": "Collaboration inquiry sent successfully"}, status=status.HTTP_200_OK)
