from django.contrib import admin

from .models import Message, Notification, Template, User


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created", "modified")
    search_fields = ("id", "name", "description")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "subject", "created", "modified")
    search_fields = ("id", "name", "body", "subject")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "is_instant",
        "schedule_at",
        "template",
        "message",
        "created",
        "modified",
    )
    search_fields = ("id", "template", "message")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "login", "email")
    search_fields = ("id", "login", "email")
