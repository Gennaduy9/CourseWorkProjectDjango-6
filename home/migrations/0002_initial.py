# Generated by Django 4.2.7 on 2023-11-05 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("message_email", "0001_initial"),
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="homeclient",
            name="mailings",
            field=models.ManyToManyField(
                related_name="messages",
                to="message_email.message",
                verbose_name="Сообщении",
            ),
        ),
        migrations.AddField(
            model_name="homeclient",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]