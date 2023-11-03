from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


#
class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test1234', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course
        )

    def test_create_lesson(self):
        url = reverse('course:lesson-create')
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'url': 'https://www.youtube.com/testlesson',
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        url = reverse('course:lesson-detail', args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        url = reverse('course:lesson-update', args=[self.lesson.id])
        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Lesson Description',
            'url': 'https://www.youtube.com/testlesson',
            'course': self.course.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        url = reverse('course:lesson-delete', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test1234', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=self.user
        )

    def test_subscribe_to_course(self):
        url = reverse('course:subscribe-course', args=[self.course.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('course:unsubscribe-course', args=[self.course.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())


