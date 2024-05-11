from django.db import models
from django.utils.translation import gettext_lazy as _


class EventTypeChoice(models.IntegerChoices):
    DIRECT = 0, _("Direct")
    FILM_ADDED = 1, _("Film added")
    ACCOUNT_ACTIVATED = 2, _("Account activated")


class NotificationChannelTypeChoice(models.IntegerChoices):
    EMAIL = 0, _("Email")
    SMS = 1, _("SMS")
    PUSH = 2, _("Push")


class NotificationStatusChoice(models.IntegerChoices):
    PENDING = 0, _("Pending")
    STARTED = 1, _("Started")
    IN_PROGRESS = 2, _("In progress")
    COMPLETED = 3, _("Completed")
    CANCELLED = 4, _("Cancelled")
    SCHEDULED = 5, _("Scheduled")
