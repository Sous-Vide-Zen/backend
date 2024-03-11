from rest_framework.routers import DefaultRouter

from src.apps.reactions.views import RecipeReactionViewSet

router = DefaultRouter()
router.register(
    r"recipe/(?P<slug>[^/.]+)/reactions", RecipeReactionViewSet, basename="reactions"
)

urlpatterns = router.urls
