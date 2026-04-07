from rest_framework import viewsets

from contact_us.models import JobCategory
from contact_us.serializers.job_category import (
    JobCategoryCreateSerializer,
    JobCategoryDetailSerializer,
    JobCategoryListSerializer,
    JobCategoryUpdateSerializer,
)


class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategoryDetailSerializer
    list_serializer_class = JobCategoryListSerializer
    create_serializer_class = JobCategoryCreateSerializer
    update_serializer_class = JobCategoryUpdateSerializer
    partial_update_serializer_class = JobCategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
