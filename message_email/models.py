from django.db import models

from home.models import HomeClient
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    TIME_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('finished', 'Завершена'),
    )

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    send_datetime = models.DateTimeField(verbose_name='Время и дата рассылки', **NULLABLE)
    frequency = models.CharField(max_length=10, choices=TIME_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES,
                              verbose_name='Статус')
    send_from_user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='user',
                                       verbose_name='Отправитель')

    send_to_client = models.ManyToManyField(to='home.HomeClient', related_name='client',
                                            verbose_name='Получатель')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    """
    Сообщение для рассылки.
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f"Сообщение {self.subject}"

    class Meta:
        permissions = [
            ("Can_view_any_newsletters", 'Can view any mailings'),
            ("You_can_disable_newsletters", 'Can disable mailings'),
            ("They_cannot_edit_mailings.", 'Cannot edit mailings.'),
            ("Can't_manage_the_mailing_list", 'Cannot manage mailing list'),
            ("Cannot_change_mailings_and_messages", 'Cannot change mailings and messages'),
        ]
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class EmailLog(models.Model):
    mailing = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='время последней попытки')
    status = models.CharField(max_length=20)
    server_response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f"Лог рассылки {self.mailing}"

    class Meta:
        verbose_name = 'Логи рассылка'
        verbose_name_plural = 'Логи рассылки'
