from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics

from .filters import PaymentFilter
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from course.permissions import IsOwner, IsModerator


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        action_permissions = {
            'retrieve': [IsOwner | IsModerator | IsAdminUser],
            'create': [IsAdminUser],
            'destroy': [IsOwner | IsAdminUser],
            'update': [IsOwner | IsModerator | IsAdminUser],
        }

        default_permissions = [IsAuthenticated]

        return [permission() for permission in action_permissions.get(self.action, default_permissions)]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]
