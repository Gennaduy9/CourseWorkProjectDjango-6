import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from message_email.models import Message, EmailLog


class Command(BaseCommand):
    help = 'Command for send mailing'

    def add_arguments(self, parser):
        parser.add_argument('mailing_pk', type=int, help='mailing_pk')

    def handle(self, *args, **options):
        print('я сработал')
        mailing = Message.objects.get(pk=options['mailing_pk'])
        try:
            send_mail(subject=mailing.letter.subject, message=mailing.letter.body,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=mailing.recipients.all())
            status = True
            server_answer = 'Email sent successfully'
        except Exception as e:
            status = False
            server_answer = str(e)
        EmailLog.objects.create(
            status=status,
            server_answer=server_answer,
            mailing=mailing,
            last_time=datetime.datetime.now())