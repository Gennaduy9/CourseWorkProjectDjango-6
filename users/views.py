from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from users.services import generate_verification_token


class UserLoginView(BaseLoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login_form.html'
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_active:
            messages.error(
                self.request,
                message='Ваша учетная запись не активирована. Пожалуйста, проверьте свою электронную почту.'
            )

        return super().form_valid(form)


class UserLogoutView(BaseLogoutView):
    pass


def user_registration_success(request):
    return render(request, template_name='users/registration_success.html')


def user_verification_view(request, pk, token):
    user = get_object_or_404(User, pk=pk, verification_token=token)
    user.is_active = True
    user.verification_token = None
    user.save()
    return redirect('users:login')


class UserRegistrationCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration_form.html'
    success_url = reverse_lazy('users:registration_success')

    def form_valid(self, form):
        new_user = form.save()
        verification_token = generate_verification_token()
        new_user.verification_token = verification_token
        new_user.save()

        verification_url = self.request.build_absolute_uri(
            reverse(
                viewname='users:verification',
                args=[new_user.pk, verification_token])
        )

        send_mail(
            subject='Успешная регистрация на почтовом сервисе',
            message=f'Нажмите сюда, чтобы активировать свой профиль {verification_url}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
