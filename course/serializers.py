from rest_framework import serializers

from .models import Course, Lesson, Payment, Subscription
from .services import stripe_get_link


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    payment_link = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user

        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_payment_link(self, obj):
        return stripe_get_link(obj)

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
