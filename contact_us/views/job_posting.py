from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from contact_us.models import JobPosting
from contact_us.serializers.job_posting import (
    JobPostingCreateSerializer,
    JobPostingDetailSerializer,
    JobPostingListSerializer,
    JobPostingUpdateSerializer,
)


class JobPostingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingDetailSerializer
    pagination_class = JobPostingPagination
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

    def paginate_queryset(self, queryset):
        if "page" not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        qs = JobPosting.objects.all()
        is_open = self.request.query_params.get("is_open")
        if is_open is not None:
            if is_open.lower() in ("true", "1"):
                qs = qs.filter(is_open=True)
            elif is_open.lower() in ("false", "0"):
                qs = qs.filter(is_open=False)
        job_type = self.request.query_params.get("type")
        if job_type:
            qs = qs.filter(type=job_type)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)
        return qs
