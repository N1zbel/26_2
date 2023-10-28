from django.core.management import BaseCommand

from course.models import Payment, Lesson, Course


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
