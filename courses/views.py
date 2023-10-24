from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics

from courses.models import Course, Lesson, Payments
from courses.serializers import CourseSerializers, LessonSerializers, PaymentsSerializer, CourseCreateSerializers


class CourseViewSet(viewsets.ModelViewSet):
    default_serializer_class = CourseSerializers
    queryset = Course.objects.all()
    serializers = {
        'create': CourseCreateSerializers,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializers


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonDestroyView(generics.DestroyAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('date_payment',)
