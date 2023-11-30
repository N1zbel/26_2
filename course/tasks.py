from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from celery import shared_task
from django.core.mail import EmailMessage

from .models import User, Course


@shared_task
def course_update_mail(course_id: int, obj=None) -> None:
    course = Course.objects.get(pk=course_id)

    recipient_list = [
        subscription.user
        for subscription in course.subscription_set.all()
    ]

    if recipient_list:
        subject = f'Обновление курса {obj.title}'
        message = 'Произошло обновление курса'
        from_email = settings.EMAIL_HOST_USER
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()

@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(
        last_login__lte=one_month_ago, is_active=True
    ).update(is_active=False)