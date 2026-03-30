from django_bolt.serializers import Serializer


class JobPostingSerializer(Serializer):
    id: int
    title: str
    category: int
    type: str
    location: str | None = None
    description: str | None = None
    responsibilities: list[str] | None = None
    qualifications: list[str] | None = None
    is_open: bool = True
    published_at: str | None = None

    class Config:
        field_sets = {
            "list": ["id", "title", "category", "type", "is_open"],
            "detail": [
                "id",
                "title",
                "category",
                "type",
                "location",
                "description",
                "responsibilities",
                "qualifications",
                "is_open",
                "published_at",
            ],
            "create": [
                "title",
                "category",
                "type",
                "location",
                "description",
                "responsibilities",
                "qualifications",
                "is_open",
                "published_at",
            ],
            "update": [
                "title",
                "category",
                "type",
                "location",
                "description",
                "responsibilities",
                "qualifications",
                "is_open",
                "published_at",
            ],
            "admin": [
                "id",
                "title",
                "category",
                "type",
                "location",
                "description",
                "responsibilities",
                "qualifications",
                "is_open",
                "published_at",
            ],
        }


JobPostingListSerializer = JobPostingSerializer.fields("list")
JobPostingDetailSerializer = JobPostingSerializer.fields("detail")
JobPostingCreateSerializer = JobPostingSerializer.fields("create")
JobPostingUpdateSerializer = JobPostingSerializer.fields("update")
