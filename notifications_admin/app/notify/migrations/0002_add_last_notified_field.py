# Generated by Django 5.0.4 on 2024-05-12 08:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notify", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recurringnotification",
            name="last_notified",
            field=models.DateTimeField(null=True),
        ),
    ]
