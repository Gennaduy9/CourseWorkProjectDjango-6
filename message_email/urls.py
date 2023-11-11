from django.urls import path

from message_email.apps import MessageEmailConfig
from message_email.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingListView

app_name = MessageEmailConfig.name

urlpatterns = [
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

]