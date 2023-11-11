from django import forms
from django.core.exceptions import ValidationError

from .models import HomeClient


class ClientForm(forms.ModelForm):
    class Meta:
        model = HomeClient
        fields = ('full_name', 'email', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваша ФИО"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваша электронная почта"})
        self.fields['comment'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваш комментарий"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) > 30:
            raise ValidationError("Электронная почта может содержать не более 30 символов")
        if '@' not in email:
            raise ValidationError("Электронная почта невозможна без '@'.")
        return email