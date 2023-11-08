from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .filters import PaymentFilter
from .models import Course, Lesson, Payment, Subscription
from .paginators import CoursePaginator, LessonPaginator
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from course.permissions import IsOwner, IsModerator


class LessonListAPIView(ListAPIView):
    """
            Представление для получения списка всех уроков.

            Атрибуты:
                serializer_class : Сериализатор для преобразования объектов урока в формат JSON.
                queryset : Набор объектов уроков, используемых для построения списка.
                pagination_class : Пагинатор, для отображения уроков на странице.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator


class LessonCreateAPIView(CreateAPIView):
    """
            Представление для создания нового урока.

            Атрибуты:
                serializer_class : Сериализатор для преобразования JSON в объект урока.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class LessonDestroyAPIView(DestroyAPIView):
    """
            Представление для удаления урока.

            Атрибуты:
                queryset: Набор уроков, для поиска урока, который требуется удалить.
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class LessonUpdateAPIView(UpdateAPIView):
    """
            Представление для обновления урока.

            Атрибуты:
                serializer_class: Сериализатор для преобразования JSON в объект урока.
                queryset: Набор уроков, для поиска урока, который требуется обновить.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonRetrieveAPIView(RetrieveAPIView):
    """
            Представление на получение деталей урока.

            Атрибуты:
                serializer_class: Сериализатор для преобразования объекта урока в JSON.
                queryset: Набор уроков, для поиска урока, и получение его детализации.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    """
            ViewSet для взаимодействия с моделью курс.

            Атрибуты:
                queryset : Набор курсов, включая связанные уроки.
                serializer_class : Сериализатор для преобразования объектов курса в JSON и наоборот.
                pagination_class : Пагинатор, для отображения курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

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


class SubscribeCourseView(generics.CreateAPIView):
    """
        Создает подписку на выбранный курс.

        Параметры:
            course_id : Идентификатор курса.

        Returns:
            Response: Объект ответа с информацией о результате операции.
                HTTP_400_BAD_REQUEST: Подписка уже есть.
                HTTP_201_CREATED: Вы подписались на курс.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)

        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'Вы уже подписаны'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'user': request.user.id, 'course': course.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'detail': 'Вы подписались на курс.'}, status=status.HTTP_201_CREATED)


class UnsubscribeCourseView(generics.DestroyAPIView):
    """
        Удаляет подписку на выбранный курс.

        Параметры:
            course_id : Идентификатор курса.

        Returns:
            Response: Ответ результата операции.
                HTTP_200_OK: Подписка удалена.
        """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Вы отписались от курса.'}, status=status.HTTP_200_OK)
