from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from home.forms import ClientForm
from home.models import HomeClient


class IndexView(TemplateView):
    template_name = 'home/index.html'
    extra_context = {
        'title': 'Сервис',
        'comment': 'Российский сервис рассылки писем на e-mail.'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = HomeClient.objects.all()[:0]
        return context_data


class CategoryListView(LoginRequiredMixin, ListView):
    model = HomeClient
    template_name = 'home/category_list.html'
    extra_context = {
        'title': 'Наши клиенты'
    }

    def get_queryset(self):
        key = 'clients_list'  # |
        client_list = cache.get(key)  # |
        if client_list is None:  # |  1. кеширование списка клиентов
            client_list = HomeClient.objects.all()  # |
            cache.set(key, client_list)  # |

        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return client_list
        return HomeClient.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = HomeClient.objects.all()

        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = HomeClient
    template_name = 'home/clients_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        client_id = self.kwargs.get('pk')
        client_item = HomeClient.objects.get(id=client_id)

        context['client_pk'] = client_id
        context['title'] = f'Наш клиент {client_item.full_name}'

        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = HomeClient
    form_class = ClientForm
    template_name = 'home/client_form.html'
    success_url = reverse_lazy('client:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = HomeClient
    form_class = ClientForm
    template_name = 'home/client_form.html'
    success_url = reverse_lazy('client:message_list')
    permission_required = []

    def has_permission(self):
        client = self.get_object()
        if self.request.user == client.user:
            return super().has_permission()


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = HomeClient
    template_name = 'home/client_confirm_delete.html'
    success_url = reverse_lazy('client:message_list')
    permission_required = []

    def has_permission(self):
        email = self.get_object()
        if self.request.user == email.user:
            return super().has_permission()
