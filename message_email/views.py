from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from message_email.forms import MessageForm
from message_email.models import Message


class MailingListView(TemplateView):
    template_name = 'message_email/mailing_list.html'
    extra_context = {
        'title': 'Наши рассылки'
    }

    def get_queryset(self):
        """Отображает конкретные письма в зависимости от того, кто является пользователем запроса."""
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return Message.objects.all()
        return Message.objects.filter(send_from_user=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message_email/message_list.html'
    permission_required = []
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):
        """Отображает конкретные письма в зависимости от того, кто является пользователем запроса."""
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return Message.objects.all()
        return Message.objects.filter(send_from_user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_email/message_form.html'
    success_url = reverse_lazy('email:message_list')

    def get_form_kwargs(self):
        """Отправляем id пользователя в form.py, чтобы мы могли показывать только клиентов этого пользователя."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Сохранение электронного письма с id пользователя из запроса"""
        if form.is_valid():
            form.instance.send_from_user = self.request.user
            form.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_email/message_form.html'
    success_url = reverse_lazy('email:message_list')
    permission_required = []

    def has_permission(self):
        """Предоставляет разрешение по конкретному запросу пользователей."""
        email = self.get_object()
        if self.request.user == email.send_from_user or self.request.user.groups.filter(name='manager').exists():
            return True
        if self.request.user == email.send_to_user:
            return True
        return super().has_permission()

    def get_form_kwargs(self):
        """Отправляет id пользователя в form.py, чтобы мы могли показывать только клиентов этого пользователя."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        """Отображает конкретную форму в зависимости от того, кто является пользователем запроса."""
        if self.request.user == self.object.send_from_user or self.request.user.groups.filter(name='manager').exists():
            return MessageForm
        elif self.request.user == self.object.send_from_user:
            return MessageForm
        else:
            return None


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = 'message_email/message_confirm_delete.html'
    success_url = reverse_lazy('email:message_list')
    permission_required = []

    def has_permission(self):
        """Предоставляет разрешение по конкретному запросу пользователей."""
        email = self.get_object()
        if self.request.user == email.send_from_user:
            return super().has_permission()
