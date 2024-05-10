from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from notify.models.mixins import TimeStampedMixin, UUIDMixin


class Roles:
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    USER = "user"


class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None):
        if not login:
            raise ValueError("User")

        user = self.model(login=login)
        user.set_password(password)
        user.email = self.normalize_email(user.email)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None):
        user = self.create_user(login, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


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
