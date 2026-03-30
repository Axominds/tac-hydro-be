from django_bolt.views import ModelViewSet

from contact_us.models import JobCategory
from contact_us.serializers.job_category import (
    JobCategoryDetailSerializer,
    JobCategoryListSerializer,
)


class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategoryDetailSerializer
    list_serializer_class = JobCategoryListSerializer
