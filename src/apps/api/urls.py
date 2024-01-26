from django.urls import include, path

urlpatterns = [
    path("", include("src.apps.users.routes.social_urls")),
    path("", include("src.apps.users.routes.django_urls")),
    path("", include("src.apps.swagger.routes")),
    path("", include("src.apps.feed.urls")),
]
