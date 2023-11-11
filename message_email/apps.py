from django.apps import AppConfig


class MessageEmailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "message_email"
    verbose_name = 'Сообщение по электронной почте'
