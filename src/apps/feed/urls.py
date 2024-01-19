from .apiviews import FeedUserList
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", FeedUserList, basename="feed")

urlpatterns = router.urls
