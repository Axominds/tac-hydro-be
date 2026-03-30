from django_bolt.views import ModelViewSet

from contact_us.models import JobApplication
from contact_us.serializers.job_application import (
    JobApplicationDetailSerializer,
    JobApplicationListSerializer,
)


class JobApplicationViewSet(ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationDetailSerializer
    list_serializer_class = JobApplicationListSerializer
