from django_bolt.views import ModelViewSet

from home.models import NewsCategory
from home.serializers.news_category import (
    NewsCategoryDetailSerializer,
    NewsCategoryListSerializer,
)


class NewsCategoryViewSet(ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategoryDetailSerializer
    list_serializer_class = NewsCategoryListSerializer
