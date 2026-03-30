from datetime import date, datetime

from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class NewsSerializer(Serializer):
    id: int
    title: str
    news_category_id: int
    news_date: date
    published_at: datetime | None = None
    summary: str | None = None
    content_html: str | None = None
    is_published: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @computed_field
    def image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        print(f"hey {instance}", flush=True)
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/image/"

    class Config:
        field_sets = {
            "list": ["id", "title", "news_date", "image", "summary"],
            "retrieve": [
                "id",
                "title",
                "news_category_id",
                "news_date",
                "image",
                "published_at",
                "summary",
                "content_html",
                "is_published",
                "created_at",
                "updated_at",
            ],
            "create": [
                "title",
                "news_category_id",
                "news_date",
                "published_at",
                "summary",
                "content_html",
                "is_published",
            ],
            "update": [
                "title",
                "news_category_id",
                "news_date",
                "published_at",
                "summary",
                "content_html",
                "is_published",
            ],
            "admin": [
                "id",
                "title",
                "news_category_id",
                "news_date",
                "published_at",
                "summary",
                "content_html",
                "is_published",
                "created_at",
                "updated_at",
            ],
        }


NewsListSerializer = NewsSerializer.fields("list")
NewsRetrieveSerializer = NewsSerializer.fields("retrieve")
NewsCreateSerializer = NewsSerializer.fields("create")
NewsUpdateSerializer = NewsSerializer.fields("update")
