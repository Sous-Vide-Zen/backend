from .apiviews import FeedPopularList
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"popular", FeedPopularList, basename="popular")

urlpatterns = router.urls
