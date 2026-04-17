from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from home.models import News
from home.serializers.news import (
    NewsCreateSerializer,
    NewsListSerializer,
    NewsRetrieveSerializer,
    NewsUpdateSerializer,
)


class ArticlePagination(PageNumberPagination):
    page_size = 3
    max_page_size = 100
    page_size_query_param = "page_size"


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsRetrieveSerializer
    list_serializer_class = NewsListSerializer
    create_serializer_class = NewsCreateSerializer
    update_serializer_class = NewsUpdateSerializer
    partial_update_serializer_class = NewsUpdateSerializer
    pagination_class = ArticlePagination

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = News.objects.all()
        news_category_id = self.request.query_params.get("news_category_id")
        if news_category_id:
            queryset = queryset.filter(news_category_id=news_category_id)
        is_published = self.request.query_params.get("is_published")
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published.lower() == "true")
        return queryset

    @action(detail=False, methods=["get"])
    def counts(self, request):
        all_news = News.objects.all()
        published = all_news.filter(is_published=True)
        drafts = all_news.filter(is_published=False)

        by_category = {}
        for cat_id in all_news.values_list("news_category_id", flat=True).distinct():
            by_category[cat_id] = all_news.filter(news_category_id=cat_id).count()

        return Response({
            "all": all_news.count(),
            "published": published.count(),
            "drafts": drafts.count(),
            "by_category": by_category,
        })

    @action(detail=True, methods=["post"], url_path="image_upload")
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        instance.image = file
        instance.save()
        return Response({"detail": "Image uploaded successfully"})
