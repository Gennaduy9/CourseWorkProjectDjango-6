from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='admin@mail.com',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        superuser.set_password('123qwe456rty')
        superuser.save()

        manager = User.objects.create(
            email='manager@sky.com',
            is_active=True,
            is_staff=True,
            is_superuser=False
        )

        manager.set_password('123qwe456rty')
        manager.save()

        user1 = User.objects.create(
            email='user1@sky.com',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )

        user1.set_password('user1')
        user1.save()

        user2 = User.objects.create(
            email='user2@sky.com',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )

        user2.set_password('user2')
        user2.save()

        view_email = Permission.objects.get(codename='view_email')
        change_email = Permission.objects.get(codename='change_email')
        view_user = Permission.objects.get(codename='view_user')
        change_user = Permission.objects.get(codename='change_user')

        manager_group, created = Group.objects.get_or_create(name='manager')
        manager_group.permissions.add(view_email, change_email, view_user, change_user)
        manager.groups.add(manager_group)