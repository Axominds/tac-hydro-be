from rest_framework import viewsets

from contact_us.models import JobPosting
from contact_us.serializers.job_posting import (
    JobPostingCreateSerializer,
    JobPostingDetailSerializer,
    JobPostingListSerializer,
    JobPostingUpdateSerializer,
)


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingDetailSerializer
    list_serializer_class = JobPostingListSerializer
    create_serializer_class = JobPostingCreateSerializer
    update_serializer_class = JobPostingUpdateSerializer
    partial_update_serializer_class = JobPostingUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
