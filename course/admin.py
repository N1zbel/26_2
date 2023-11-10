from django.contrib import admin

from .models import User, Payment, Course

admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Course)