from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Lesson, Course, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test1@test.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('test123')
        self.user.save()

        self.course = Course.objects.create(
            title='CourseTest',
            description='CourseTest',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='TestLesson',
            course=self.course,
            owner=self.user
        )

        self.subscription = Subscription.objects.create(
            course=self.course,
            user=self.user

        )

    def test_create_course(self):
        """ Тестирование создания курса"""
        data = {
            'title': 'CourseTest2',
            'owner': self.user.id,
            'description': 'CourseTest2'
        }

        response = self.client.post('/course/', data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'CourseTest2', 'description': 'CourseTest2', 'picture': None, 'owner': 1}
        )

    def test_list_course(self):
        """ Тестирование вывода списка курсов"""

        response = self.client.get('/course/')
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
                'results': [
                    {
                        'id': self.course.id,
                        'lesson_count': 1,
                        'lesson': [
                            {
                                'id': self.lesson.id,
                                'title': 'TestLesson',
                                'description': None,
                                'image': None,
                                'url': None,
                                'course': self.course.id,
                                'owner': self.user.id
                            }
                        ],
                        'subscription': [
                            {
                                'id': self.subscription.id,
                                'is_active': True,
                                'course': self.course.id,
                                'user': self.user.id
                            }
                        ],
                        'title': 'CourseTest',
                        'description': 'CourseTest',
                        'picture': None,
                        'owner': self.user.id
                    }
                    ],
                }
            )

    def test_retrieve_course(self):
        """ Тестирование вывода детальной информации по курсу"""

        response = self.client.get(f'/course/{self.course.id}/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.course.id,
                'lesson_count': 1,
                'lesson': [
                    {
                        'id': self.lesson.id,
                        'title': 'TestLesson',
                        'description': None,
                        'image': None,
                        'url': None,
                        'course': self.course.id,
                        'owner': self.user.id
                    }
                ],
                'subscription': [
                    {
                        'id': self.subscription.id,
                        'is_active': True,
                        'course': self.course.id,
                        'user': self.user.id
                    }
                ],
                'title': 'CourseTest',
                'description': 'CourseTest',
                'picture': None,
                'owner': self.user.id
            }
        )

    def test_update_course(self):
        """ Тестирование полного обновления курса"""
        data = {
            'title': 'NewCourse',
            'description': 'NewCourse',
            'owner': self.user.id,
            'picture': ''
        }

        response = self.client.put(f'/course/{self.course.id}/', data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.course.id,
                'lesson_count': 1,
                'lesson': [
                    {
                        'id': self.lesson.id,
                        'title': 'TestLesson',
                        'description': None,
                        'image': None,
                        'url': None,
                        'course': self.course.id,
                        'owner': self.user.id
                    }
                ],
                'subscription': [
                    {
                        'id': self.subscription.id,
                        'is_active': True,
                        'course': self.course.id,
                        'user': self.user.id
                    }
                ],
                'title': 'NewCourse',
                'description': 'NewCourse',
                'picture': None,
                'owner': self.user.id
            }
        )

    def test_partial_update_course(self):
        """ Тестирование частичного обновления курса"""
        data = {
            'title': 'NewCourse123'
        }

        response = self.client.patch(f'/course/{self.course.id}/', data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.course.id,
                'lesson_count': 1,
                'lesson': [
                    {
                        'id': self.lesson.id,
                        'title': 'TestLesson',
                        'description': None,
                        'image': None,
                        'url': None,
                        'course': self.course.id,
                        'owner': self.user.id
                    }
                ],
                'subscription': [
                    {
                        'id': self.subscription.id,
                        'is_active': True,
                        'course': self.course.id,
                        'user': self.user.id
                    }
                ],
                'title': 'NewCourse123',
                'description': 'CourseTest',
                'picture': None,
                'owner': self.user.id
            }
        )

    def test_delete_course(self):
        """ Тестирование удаления курса"""

        response = self.client.delete(f'/course/{self.course.id}/')
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(Course.objects.all().exists())
