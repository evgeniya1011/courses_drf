from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from courses.models import Course, Lesson, Payments
from courses.serializers import CourseSerializers, LessonSerializers, PaymentsSerializer, CourseCreateSerializers
from users.permissions import IsModerator, IsNotModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'UPDATE']:
            self.permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super(CourseViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        self.serializer_class = CourseCreateSerializers
        new_course = super().create(request, *args, **kwargs)
        new_course.owner = self.request.user
        new_course.save()
        return new_course



class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyView(generics.DestroyAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator | IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('date_payment',)
