from config.settings import DEBUG
from django.contrib import admin
from django.urls import include, path

#TODO: Fix urls
urlpatterns = [
    path("notifications/admin/", admin.site.urls),
    path("notifications/tinymce/", include("tinymce.urls")),
]

if DEBUG:
    urlpatterns += [path("notifications/__debug__/", include("debug_toolbar.urls"))]
