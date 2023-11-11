from django.contrib import admin

from home.models import HomeClient
from users.models import User

admin.site.register(User)


@admin.register(HomeClient)
class HomeClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'email', 'comment',)
