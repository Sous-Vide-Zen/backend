from django.urls import include, path

urlpatterns = [
    path("", include("src.apps.swagger.routes")),
]
