from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class SiteSettingsSerializer(Serializer):
    id: int
    company_name: str
    tagline: str | None = None
    address: str | None = None
    phone: str | None = None
    contact_email: str | None = None
    collaboration_email: str | None = None
    business_hours: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None
    map_embed_url: str | None = None
    organization_chart_image_path: str | None = None
    founded_year: int | None = None

    @computed_field
    def organization_chart_image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/organization_chart_image/"

    class Config:
        field_sets = {
            "list": [
                "id",
                "company_name",
                "tagline",
                "address",
                "phone",
                "contact_email",
                "collaboration_email",
                "business_hours",
                "facebook_url",
                "linkedin_url",
                "map_embed_url",
                "organization_chart_image",
                "founded_year",
            ],
            "detail": [
                "id",
                "company_name",
                "tagline",
                "address",
                "phone",
                "contact_email",
                "collaboration_email",
                "business_hours",
                "facebook_url",
                "linkedin_url",
                "map_embed_url",
                "organization_chart_image",
                "founded_year",
            ],
            "create": [
                "company_name",
                "tagline",
                "address",
                "phone",
                "contact_email",
                "collaboration_email",
                "business_hours",
                "facebook_url",
                "linkedin_url",
                "map_embed_url",
                "founded_year",
            ],
            "update": [
                "company_name",
                "tagline",
                "address",
                "phone",
                "contact_email",
                "collaboration_email",
                "business_hours",
                "facebook_url",
                "linkedin_url",
                "map_embed_url",
                "founded_year",
            ],
            "admin": [
                "id",
                "company_name",
                "tagline",
                "address",
                "phone",
                "contact_email",
                "collaboration_email",
                "business_hours",
                "facebook_url",
                "linkedin_url",
                "map_embed_url",
                "organization_chart_image_path",
                "founded_year",
            ],
        }


SiteSettingsListSerializer = SiteSettingsSerializer.fields("list")
SiteSettingsDetailSerializer = SiteSettingsSerializer.fields("detail")
SiteSettingsCreateSerializer = SiteSettingsSerializer.fields("create")
SiteSettingsUpdateSerializer = SiteSettingsSerializer.fields("update")
