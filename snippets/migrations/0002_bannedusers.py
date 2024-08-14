# Generated by Django 5.1 on 2024-08-11 03:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("snippets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BannedUsers",
            fields=[
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="banned_users",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                        unique=True,
                    ),
                ),
            ],
        ),
    ]
