from django.urls import include, path
from movies.api.v1 import views
from movies.api.v1.views import MoviesApi
from rest_framework.routers import DefaultRouter

# urlpatterns = [path("movies/", MoviesListApi.as_view())]

router = DefaultRouter()
router.register("movies", MoviesApi)

urlpatterns = [path("", include(router.urls))]
