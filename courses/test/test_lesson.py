from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('test123')
        self.user.save()

        self.course = Course.objects.create(
            title='CourseTest'
        )

        self.lesson = Lesson.objects.create(
            title='Test',
            course=self.course,
            owner=self.user)

    def test_create_lesson(self):
        """ Тестирование создания уроков"""
        data = {
            'title': 'Test2',
            'owner': self.user.id,
            'course': self.course.id,
            'url': 'https://www.youtube.com/'
        }

        response = self.client.post(reverse('courses:lesson_create'), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                'id': response.json()['id'],
                'title': 'Test2',
                'description': None,
                'image': None,
                'url': 'https://www.youtube.com/',
                'course': self.course.id,
                'owner': self.user.id}
        )

    def test_list_lesson(self):
        """ Тестирование вывода списка уроков"""

        response = self.client.get(reverse('courses:lesson_list'))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [{
                    'id': self.lesson.id,
                    'title': 'Test',
                    'description': None,
                    'image': None,
                    'url': None,
                    'course': self.course.id,
                    'owner': self.user.id
                }
                ]
            }
        )

    def test_retrieve_lesson(self):
        """ Тестирование вывода детальной информации по уроку"""

        url = reverse('courses:lesson_detail', kwargs={'pk': self.lesson.id})

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'title': 'Test', 'description': None, 'image': None, 'url': None,
             'course': self.course.id, 'owner': self.user.id}
        )

    def test_update_lesson(self):
        """ Тестирование полного обновления урока"""
        data = {
            'title': 'NewTest',
            'description': 'NewTest',
            'owner': self.user.id,
            'course': self.course.id,
            'url': 'https://www.youtube.com/hguu/',
            'image': ''
        }

        response = self.client.put(reverse('courses:lesson_update', kwargs={'pk': self.lesson.id}), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'NewTest',
                'description': 'NewTest',
                'image': None,
                'url': 'https://www.youtube.com/hguu/',
                'course': self.course.id,
                'owner': self.user.id
            }
        )

    def test_partial_update_lesson(self):
        """ Тестирование частичного обновления урока"""
        data = {
            'title': 'NewTest11'
        }

        response = self.client.patch(reverse('courses:lesson_update', kwargs={'pk': self.lesson.id}), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'NewTest11',
                'description': None,
                'image': None,
                'url': None,
                'course': self.course.id,
                'owner': self.user.id
            }
        )

    def test_delete_lesson(self):
        """ Тестирование удаления урока"""

        response = self.client.delete(reverse('courses:lesson_delete', kwargs={'pk': self.lesson.id}))
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(Lesson.objects.all().exists())

    def tearDown(self):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()
