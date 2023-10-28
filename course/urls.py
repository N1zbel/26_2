from rest_framework.routers import DefaultRouter
from django.urls import path
from course.views import LessonListAPIView, LessonCreateAPIView, LessonDestroyAPIView, LessonUpdateAPIView, \
    LessonRetrieveAPIView, CourseViewSet

app_name = 'course'

router = DefaultRouter()
router.register(r'course', CourseViewSet)

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
] + router.urls
