from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class UserRoles(models.TextChoices):
    MEMBER = 'member', gettext_lazy('member')
    MODERATOR = 'moderator', gettext_lazy('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    country = models.CharField(max_length=20, verbose_name='Страна')
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
