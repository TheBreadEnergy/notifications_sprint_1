from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from notify.grpc.utils import GrpcClient
from notify.models.enums import (EventTypeChoice,
                                 NotificationChannelTypeChoice,
                                 NotificationStatusChoice)
from notify.models.mixins import TimeStampedMixin, UUIDMixin
from tinymce import models as tinymce_models


class Template(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    layout = tinymce_models.HTMLField(_("layout"))
    event_type = models.IntegerField(
        choices=EventTypeChoice.choices,
        default=EventTypeChoice.DIRECT,
        null=False,
    )

    class Meta:
        db_table = 'content"."templates'
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self) -> str:
        return str(self.name)


class NotificationBase(TimeStampedMixin, UUIDMixin):
    template = models.ForeignKey(
        "Template",
        on_delete=models.CASCADE,
        verbose_name=_("Template"),
    )
    user_ids = ArrayField(models.UUIDField(), verbose_name=_("User IDs"))
    notification_channel_type = models.IntegerField(
        choices=NotificationChannelTypeChoice.choices,
        default=NotificationChannelTypeChoice.EMAIL,
        null=False,
    )
    subject = models.CharField(_("Subject"), max_length=255)
    text = models.TextField(_("Text"))
    status = models.IntegerField(
        choices=NotificationStatusChoice.choices,
        default=NotificationStatusChoice.PENDING,
        null=False,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)


class InstantNotification(NotificationBase):
    class Meta:
        db_table = 'content"."instant_notifications'
        verbose_name = _("Instant notification")
        verbose_name_plural = _("Instant notifications")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        GrpcClient.send_instant_notification(self)


class ScheduledNotification(NotificationBase):
    scheduled_at = models.DateTimeField()

    class Meta:
        db_table = 'content"."scheduled_notifications'
        verbose_name = _("Scheduled notification")
        verbose_name_plural = _("Scheduled notifications")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        GrpcClient.create_scheduled_notification(self)


class RecurringNotification(NotificationBase):
    cron_string = models.TextField(_("Cron string"))

    class Meta:
        db_table = 'content"."recurring_notifications'
        verbose_name = _("Recurring notification")
        verbose_name_plural = _("Recurring notifications")
