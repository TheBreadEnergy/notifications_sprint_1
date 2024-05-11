from django.contrib import admin

from .models import (InstantNotification, RecurringNotification,
                     ScheduledNotification, Template, User)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "event_type")
    search_fields = ("id", "name", "description")


@admin.register(InstantNotification)
class InstantNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "subject",
        "template",
        "created",
        "modified",
    )
    search_fields = (
        "id",
        "template",
        "subject",
    )


@admin.register(ScheduledNotification)
class ScheduledNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "subject",
        "template",
        "scheduled_at",
        "created",
        "modified",
    )
    search_fields = (
        "id",
        "template",
        "subject",
        "scheduled_at",
    )


@admin.register(RecurringNotification)
class RecurringNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "subject",
        "template",
        "cron_string",
        "created",
        "modified",
    )
    search_fields = (
        "id",
        "template",
        "subject",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "login", "email")
    search_fields = ("id", "login", "email")
