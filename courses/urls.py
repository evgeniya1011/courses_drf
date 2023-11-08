from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig

from courses.views import CourseViewSet, LessonCreateView, LessonRetrieveView, LessonUpdateView, LessonListView, \
    LessonDestroyView, PaymentsListAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView, \
    PaymentsCreateAPIView, PaymentsRetrieveAPIView

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
    path('payment/create/', PaymentsCreateAPIView.as_view(), name='payment-create'),
    path('payment/retrieve/<str:payment_id>/', PaymentsRetrieveAPIView.as_view(), name='payment-retrieve'),

    path('subs/create/', SubscriptionCreateAPIView.as_view(), name='sub-create'),
    path('subs/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='sub-delete'),


] + router.urls
