from django_bolt.views import ModelViewSet

from contact_us.models import JobPosting
from contact_us.serializers.job_posting import (
    JobPostingDetailSerializer,
    JobPostingListSerializer,
)


class JobPostingViewSet(ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingDetailSerializer
    list_serializer_class = JobPostingListSerializer
