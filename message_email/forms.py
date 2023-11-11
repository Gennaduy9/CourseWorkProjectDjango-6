from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware

from home.models import HomeClient
from .models import Message


class MessageForm(forms.ModelForm):
    """Форма для электронной почты использует виджеты классов начальной загрузки и проверяет некоторые поля."""

    class Meta:
        model = Message
        fields = (
            'subject', 'message', 'send_to_client', 'frequency', 'status', 'send_datetime', 'is_active',)

        widgets = {
            'send_datetime': forms.DateTimeInput(
                attrs={"class": "form-control", 'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        # in CreateView we added user = self.request.user
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['send_to_client'].queryset = HomeClient.objects.filter(user=user)

        self.fields['subject'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите тему письма"})
        self.fields['message'].widget.attrs.update(
            {"class": "form-control", "rows": 5, "placeholder": "Напишите свое сообщение"})
        self.fields['frequency'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['status'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['send_to_client'].widget.attrs.update(
            {"class": "form-control"})

    # def clean_send_datetime(self):
    #     send_datetime = self.cleaned_data['send_datetime']
    #     cur_datetime = datetime.now() + timedelta(hours=5)
    #
    #     if send_datetime < cur_datetime:
    #         raise ValidationError("Вы не можете отправлять электронные письма в прошлом.")
    #
    #     return send_datetime

    def clean(self):
        """Преобразует дату и время в правильный формат."""
        cleaned_data = super().clean()
        send_date = cleaned_data.get('send_date')
        if send_date:
            cleaned_data['send_date'] = make_aware(send_date)
        return cleaned_data


