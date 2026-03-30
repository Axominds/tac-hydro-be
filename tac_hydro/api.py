from __future__ import annotations

from django.apps import apps
from django_bolt import BoltAPI
from django_bolt.responses import FileResponse
from django_bolt.views import APIView

from about_us.views import (
    AboutPageSectionViewSet,
    CorePrinciplesIntroViewSet,
    CorePrincipleViewSet,
    TeamCategoryViewSet,
    TeamMemberCategoryViewSet,
    TeamMemberViewSet,
)
from contact_us.views import (
    InitiateSynergySectionViewSet,
    JobApplicationViewSet,
    JobCategoryViewSet,
    JobPostingViewSet,
    PartnershipRoadmapSectionViewSet,
    PartnershipRoadmapStepViewSet,
)
from galleries.views import (
    GalleryCategoryViewSet,
    GalleryImageViewSet,
    GallerySubcategoryViewSet,
)
from home.views import (
    BannerViewSet,
    NewsAttachmentViewSet,
    NewsCategoryViewSet,
    NewsViewSet,
    SiteSettingsViewSet,
    ValuedPartnerViewSet,
)
from home.views.stats import StatsView
from projects.views import (
    ProjectScopeImageViewSet,
    ProjectScopeMembershipViewSet,
    ProjectScopeViewSet,
    ProjectViewSet,
)
from services.views import (
    ExpertiseCategoryViewSet,
    ExpertiseItemViewSet,
    ServiceSectorViewSet,
)
from tac_hydro.extras import MEDIA_ROOT

api = BoltAPI(prefix="/api", trailing_slash="append")

api.viewset("/home/settings")(SiteSettingsViewSet)
api.viewset("/home/banners")(BannerViewSet)
api.viewset("/home/valued-partners")(ValuedPartnerViewSet)
api.viewset("/home/news-categories")(NewsCategoryViewSet)
api.viewset("/home/news")(NewsViewSet)
api.viewset("/home/news-attachments")(NewsAttachmentViewSet)
api.view("/home/stats/", methods=["GET"])(StatsView)

api.viewset("/about-us/sections")(AboutPageSectionViewSet)
api.viewset("/about-us/core-principles-intro")(CorePrinciplesIntroViewSet)
api.viewset("/about-us/core-principles")(CorePrincipleViewSet)
api.viewset("/about-us/team-categories")(TeamCategoryViewSet)
api.viewset("/about-us/team-members")(TeamMemberViewSet)
api.viewset("/about-us/team-member-categories")(TeamMemberCategoryViewSet)

api.viewset("/services/expertise-categories")(ExpertiseCategoryViewSet)
api.viewset("/services/expertise-items")(ExpertiseItemViewSet)
api.viewset("/services/sectors")(ServiceSectorViewSet)

api.viewset("/projects/scopes")(ProjectScopeViewSet)
api.viewset("/projects")(ProjectViewSet)
api.viewset("/projects/scope-memberships")(ProjectScopeMembershipViewSet)
api.viewset("/projects/scope-images")(ProjectScopeImageViewSet)

api.viewset("/galleries/categories")(GalleryCategoryViewSet)
api.viewset("/galleries/subcategories")(GallerySubcategoryViewSet)
api.viewset("/galleries/images")(GalleryImageViewSet)

api.viewset("/contact-us/partnership-roadmap-sections")(PartnershipRoadmapSectionViewSet)
api.viewset("/contact-us/partnership-roadmap-steps")(PartnershipRoadmapStepViewSet)
api.viewset("/contact-us/initiate-synergy")(InitiateSynergySectionViewSet)
api.viewset("/contact-us/job-categories")(JobCategoryViewSet)
api.viewset("/contact-us/jobs")(JobPostingViewSet)
api.viewset("/contact-us/job-applications")(JobApplicationViewSet)


class FileServeView(APIView):
    def get(self, request, app_label: str, model_name: str, pk: int, field_name: str):
        model = apps.all_models.get(app_label, {}).get(model_name)
        if model is None:
            return {"error": "Not found"}, 404

        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return {"error": "Not found"}, 404

        file_field = getattr(instance, field_name, None)
        if file_field is None or not file_field.name:
            return {"error": "No file"}, 404

        file_path = MEDIA_ROOT / file_field.name
        if not file_path.exists():
            return {"error": "File not found"}, 404
        return FileResponse(path=str(file_path), filename=file_field.name)


api.view("/{app_label}/{model_name}/{pk}/{field_name}/", methods=["GET"])(FileServeView)
