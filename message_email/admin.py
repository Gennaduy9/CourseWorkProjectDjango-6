from django.contrib import admin

from message_email.models import Message, EmailLog


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'status',)

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('status',)


