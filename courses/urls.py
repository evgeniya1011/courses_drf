from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig

from courses.views import CourseViewSet, LessonCreateView, LessonRetrieveView, LessonUpdateView, LessonListView,  LessonDestroyView, PaymentsListAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete'),
    path('lesson/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_detail'),

    path('payment/', PaymentsListAPIView.as_view(), name='payment-list'),

] + router.urls
