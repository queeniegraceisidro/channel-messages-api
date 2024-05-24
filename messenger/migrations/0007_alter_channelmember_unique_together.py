# Generated by Django 5.0.2 on 2024-05-24 05:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("messenger", "0006_channel_invite_code_alter_channelmember_member"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="channelmember",
            unique_together={("channel", "member", "deleted_at")},
        ),
    ]
