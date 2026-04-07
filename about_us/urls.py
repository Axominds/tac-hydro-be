from rest_framework.routers import DefaultRouter

from about_us.views import (
    AboutPageSectionViewSet,
    CorePrincipleViewSet,
    CorePrinciplesIntroViewSet,
    TeamCategoryViewSet,
    TeamMemberCategoryViewSet,
    TeamMemberViewSet,
)

router = DefaultRouter()
router.register(r"sections", AboutPageSectionViewSet, basename="aboutpagesection")
router.register(r"core-principles-intro", CorePrinciplesIntroViewSet, basename="coreprinciplesintro")
router.register(r"core-principles", CorePrincipleViewSet, basename="coreprinciple")
router.register(r"team-categories", TeamCategoryViewSet, basename="teamcategory")
router.register(r"team-members", TeamMemberViewSet, basename="teammember")
router.register(r"team-member-categories", TeamMemberCategoryViewSet, basename="teammembercategory")

urlpatterns = router.urls
