from config.settings import DEBUG
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("movies.api.urls")),
]

if DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
