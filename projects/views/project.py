from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from projects.models import Project
from projects.serializers.project import (
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectUpdateSerializer,
)


class ProjectPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 100


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    pagination_class = ProjectPagination
    list_serializer_class = ProjectListSerializer
    create_serializer_class = ProjectCreateSerializer
    update_serializer_class = ProjectUpdateSerializer
    partial_update_serializer_class = ProjectUpdateSerializer

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
        qs = Project.objects.all()
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)
        return qs
