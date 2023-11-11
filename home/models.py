from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class HomeClient(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(unique=False, verbose_name='Почта')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
    mailings = models.ManyToManyField(to='message_email.Message', related_name='messages', verbose_name='Сообщении')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
