from rest_framework.routers import DefaultRouter

from home.views import (
    BannerViewSet,
    NewsAttachmentViewSet,
    NewsCategoryViewSet,
    NewsViewSet,
    SiteSettingsViewSet,
    ValuedPartnerViewSet,
)

router = DefaultRouter()
router.register(r"settings", SiteSettingsViewSet, basename="sitesettings")
router.register(r"banners", BannerViewSet, basename="banner")
router.register(r"valued-partners", ValuedPartnerViewSet, basename="valuedpartner")
router.register(r"news-categories", NewsCategoryViewSet, basename="newscategory")
router.register(r"news", NewsViewSet, basename="news")
router.register(r"news-attachments", NewsAttachmentViewSet, basename="newsattachment")

urlpatterns = router.urls
