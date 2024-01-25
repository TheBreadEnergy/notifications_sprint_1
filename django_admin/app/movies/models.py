from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import FileField, constraints
from django.utils.translation import gettext_lazy as _
from movies.storage import CustomStorage
from storages.backends.s3boto3 import S3Boto3Storage


class TimeStampledMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampledMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Filmwork(UUIDMixin, TimeStampledMixin):
    class TypeChoice(models.TextChoices):
        TV_SHOW = "tv_show", _("TV_SHOW")
        MOVIE = "movie", _("MOVIE")

    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(_("description"))
    creation_date = models.DateField(_("creation date"))
    rating = models.FloatField(
        "rating", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.TextField(
        choices=TypeChoice.choices, default=TypeChoice.TV_SHOW, null=True
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField("Person", through="PersonFilmwork")
    file = FileField(storage=CustomStorage(), null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"
        indexes = [
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx")
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        indexes = [
            models.Index(fields=["genre", "film_work"], name="genre_film_work_idx")
        ]
        constraints = [
            constraints.UniqueConstraint(
                fields=["genre", "film_work"], name="genre_film_work_unique"
            )
        ]


class Person(UUIDMixin, TimeStampledMixin):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")

    full_name = models.CharField(
        _("full name"), max_length=255, blank=False, null=False
    )
    gender = models.TextField(_("gender"), choices=Gender.choices, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'


class PersonFilmwork(UUIDMixin):
    class PersonRoleChoice(models.TextChoices):
        ADMIN = "director", _("director")
        SCREENWRITER = "screenwriter", _("screenwriter")
        ACTOR = "actor", _("actor")

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="roles")
    role = models.TextField(
        _("role"), choices=PersonRoleChoice.choices, default=PersonRoleChoice.ACTOR
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        indexes = [
            models.Index(
                fields=["person", "film_work", "role"], name="person_film_work_idx"
            )
        ]
        constraints = [
            constraints.UniqueConstraint(
                fields=["person", "film_work", "role"],
                name="person_film_work_role_unique",
            )
        ]
