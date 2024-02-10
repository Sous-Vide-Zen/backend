from rest_framework.routers import DefaultRouter

from src.apps.follow.views import FollowViewSet

router = DefaultRouter()
router.register(r"user/(?P<username>[A-Za-z0-9]+)/subscriptions", FollowViewSet, basename="subscriptions")

urlpatterns = router.urls
