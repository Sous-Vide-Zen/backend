from django.urls import include, path

urlpatterns = [
    path(r'^auth/', include('djoser.urls')),
    path(r'^auth/', include('djoser.urls.authtoken')),
]