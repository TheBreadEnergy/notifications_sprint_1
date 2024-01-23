from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Case, Q, When
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import BaseListView
from movies.api.paginators import TotalPageCountPaginator
from movies.api.serializers import FilmworkSerializer
from movies.models import Filmwork, PersonFilmwork
from rest_framework import mixins, viewsets


class MoviesApi(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    queryset = (
        Filmwork.objects.all()
        .values("id", "title", "description", "creation_date", "rating", "type")
        .prefetch_related("persons", "genres")
        .annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            directors=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role=PersonFilmwork.PersonRoleChoice.ADMIN),
            ),
            actors=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role=PersonFilmwork.PersonRoleChoice.ACTOR),
            ),
            writers=ArrayAgg(
                "persons__full_name",
                filter=Q(
                    personfilmwork__role=PersonFilmwork.PersonRoleChoice.SCREENWRITER
                ),
            ),
        )
    )
    pagination_class = TotalPageCountPaginator
    serializer_class = FilmworkSerializer
