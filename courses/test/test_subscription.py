from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Subscription
from users.models import User


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('test123')
        self.user.save()

        self.course = Course.objects.create(
            title='CourseTest',
            description='CourseTest',
            owner=self.user
        )

        self.subscription = Subscription.objects.create(
            course=self.course,
            user=self.user

        )

    def test_create_subscription(self):
        """ Тестирование создания подписок"""

        self.new_course = Course.objects.create(
            title='Test',
            description='CourseTest',
            owner=self.user
        )

        data = {
            'user': self.user.id,
            'course': self.new_course.id,
            'is_active': True
        }

        response = self.client.post(reverse('courses:sub-create'), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': response.json()['id'], 'is_active': True, 'user': self.user.id, 'course': self.new_course.id}
        )

    def test_delete_lesson(self):
        """ Тестирование удаления урока"""

        response = self.client.delete(reverse('courses:sub-delete', kwargs={'pk': self.subscription.id}))
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertTrue(Subscription.objects.all().filter(is_active=False))
