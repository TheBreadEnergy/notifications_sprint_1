import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from notify.user import CustomUserManager
from tinymce.models import HTMLField


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Template(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    layout = HTMLField(_("layout"))

    class Meta:
        db_table = 'content"."templates'
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self) -> str:
        return str(self.name)


class Message(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    subject = models.CharField(_("subject"), max_length=255)
    body = models.TextField(_("body"), blank=True)

    class Meta:
        db_table = 'content"."messages'
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self) -> str:
        return str(self.name)


class Notification(UUIDMixin, TimeStampedMixin):
    template = models.ForeignKey(
        "Template",
        on_delete=models.CASCADE,
        verbose_name=_("Template"),
        related_name="notification",
    )
    message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
        verbose_name=_("Message"),
        related_name="notification",
    )
    status = models.CharField(
        _("status"),
        default="CREATED",
        max_length=10,
        editable=False,
    )
    users_ids = ArrayField(models.UUIDField(), verbose_name=_("users_ids"))
    is_instant = models.BooleanField(_("is_instant"), default=True)  # type: ignore
    schedule_at = models.DateTimeField(
        _("schedule_at"),
        default=now,
        help_text=_(
            "Укажите в случае, если вы сняли галку в пункте 'Мгновенная отправка' "
            "и хотите отправить уведомление отложенно"
        ),
    )
    additional_info = models.JSONField(
        _("additional_info"),
        default={},
        null=True,
        blank=True,
        help_text=_(
            "Любая дополнительная информация для шаблона в формате ключ-значение, например "
            "{'user_from_id': 'c9212aef-0959-4b94-aee2-5cf9c9ae6bd1'}"
        ),
    )

    class Meta:
        db_table = 'content"."notifications'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        constraints = [
            models.UniqueConstraint(
                fields=["template", "message", "users_ids", "schedule_at"],
                name="unique_notification_for_users_ids",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)


class User(UUIDMixin, AbstractBaseUser):
    login = models.CharField(verbose_name="login", max_length=255, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    objects = CustomUserManager()
    USERNAME_FIELD = "login"

    class Meta:
        db_table = 'content"."users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f"{self.email} {self.id}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
