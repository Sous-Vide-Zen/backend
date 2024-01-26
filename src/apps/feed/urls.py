from rest_framework.routers import DefaultRouter

from .views import FeedUserList

router = DefaultRouter()
router.register(r"feed", FeedUserList, basename="feed")

urlpatterns = router.urls
