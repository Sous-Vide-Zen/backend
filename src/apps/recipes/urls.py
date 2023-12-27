from rest_framework import routers
from .views import RecipeViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register("recipes", RecipeViewSet)

urlpatterns = [path("", include(router.urls))]
