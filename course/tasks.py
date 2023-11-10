from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from celery import shared_task
from django.core.mail import EmailMessage

from .models import User


@shared_task
def course_update_mail(obj):
    subject = f'Обновление курса {obj.title}'
    message = 'Произошло обновление курса'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = []
    subscription_list = obj.subscription_set.all()
    for subscription in subscription_list:
        recipient_list.append(subscription.user)

    if len(subscription_list) > 0:
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()

@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lte=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()