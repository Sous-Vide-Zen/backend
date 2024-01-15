from .apiviews import FeedSubscriptionsList, FeedPopularList, FeedUserList
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", FeedUserList, basename="feed")
router.register(r"subscriptions", FeedSubscriptionsList, basename="subscriptions")
router.register(r"popular", FeedPopularList, basename="popular")


urlpatterns = router.urls
