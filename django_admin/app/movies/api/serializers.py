from movies.models import Filmwork
from rest_framework import serializers
from rest_framework.serializers import Serializer


class FilmworkSerializer(Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    creation_date = serializers.DateField()
    description = serializers.StringRelatedField()
    type = serializers.ChoiceField(Filmwork.TypeChoice)
    rating = serializers.FloatField()
    genres = serializers.ListField()
    actors = serializers.ListField()
    directors = serializers.ListField()
    writers = serializers.ListField()
