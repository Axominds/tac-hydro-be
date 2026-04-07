from rest_framework import viewsets

from contact_us.models import JobApplication
from contact_us.serializers.job_application import (
    JobApplicationCreateSerializer,
    JobApplicationDetailSerializer,
    JobApplicationListSerializer,
    JobApplicationUpdateSerializer,
)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationDetailSerializer
    list_serializer_class = JobApplicationListSerializer
    create_serializer_class = JobApplicationCreateSerializer
    update_serializer_class = JobApplicationUpdateSerializer
    partial_update_serializer_class = JobApplicationUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
