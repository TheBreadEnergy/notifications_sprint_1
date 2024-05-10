import grpc
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from notify.grpc import managers_pb2, managers_pb2_grpc
from notify.models.mixins import TimeStampedMixin, UUIDMixin
from tinymce import models as tinymce_models


class Template(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    layout = tinymce_models.HTMLField(_("layout"))

    class Meta:
        db_table = 'content"."templates'
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self) -> str:
        return str(self.name)


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
        with grpc.insecure_channel(settings.NOTIFICATION_SERVICE_GRPC) as channel:
            stub = managers_pb2_grpc.ManagerNotificationStub(channel)
            request = managers_pb2.SendNotificationRequest(
                user_ids=[str(user_id) for user_id in self.user_ids],
                notification_id=str(self.id),
                template_id=str(self.template.id),
                subject=self.subject,
                text=self.text,
                type=self.notification_channel_type,
            )
            stub.SendNotificationToUsers(request)


class ScheduledNotification(NotificationBase):
    scheduled_at = models.DateTimeField()

    class Meta:
        db_table = 'content"."scheduled_notifications'
        verbose_name = _("Scheduled notification")
        verbose_name_plural = _("Scheduled notifications")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with grpc.insecure_channel(settings.NOTIFICATION_SERVICE_GRPC) as channel:
            stub = managers_pb2_grpc.ManagerNotificationStub(channel)
            request = managers_pb2.CreateDelayedNotificationRequest(
                user_ids=[str(user_id) for user_id in self.user_ids],
                notification_id=str(self.id),
                template_id=str(self.template.id),
                subject=self.subject,
                text=self.text,
                type=self.notification_channel_type,
                delay=int((self.scheduled_at - timezone.now()).total_seconds()), ##TODO
            )
            stub.CreateDelayedNotification(request)


class RecurringNotification(NotificationBase):
    cron_string = models.TextField(_("Cron string"))

    class Meta:
        db_table = 'content"."recurring_notifications'
        verbose_name = _("Recurring notification")
        verbose_name_plural = _("Recurring notifications")
