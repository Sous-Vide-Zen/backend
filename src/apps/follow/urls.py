from django.urls import path
from rest_framework.routers import DefaultRouter

from src.apps.follow.views import FollowViewSet, FollowerViewSet, SubscribeViewSet

router = DefaultRouter()
router.register(
    r"user/(?P<username>[A-Za-z0-9]+)/subscriptions",
    FollowViewSet,
    basename="subscriptions",
)
router.register(
    r"user/(?P<username>[A-Za-z0-9]+)/subscribers",
    FollowerViewSet,
    basename="subscriptions",
)

urlpatterns = [
    path(
        "subscribe/", SubscribeViewSet.as_view({"post": "create", "delete": "destroy"})
    ),
]

urlpatterns += router.urls
