from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_async(subject, massage, recipient_email):
    send_mail(subject, massage, 'no-replay@example.com', [recipient_email])

