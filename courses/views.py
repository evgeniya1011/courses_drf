from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, Lesson, Payments, Subscription
from courses.paginators import CoursesPaginator
from courses.serializers import CourseSerializers, LessonSerializers, PaymentsSerializer, CourseCreateSerializers, \
    SubscriptionSerializer
from courses.services import send_message_active
from users.permissions import IsModerator, IsNotModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsModerator]
    pagination_class = CoursesPaginator

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'UPDATE']:
            self.permission_classes = [IsAuthenticated, IsNotModerator | IsOwner]
        else:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super(CourseViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = CourseCreateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        # new_course = super().create(request, *args, **kwargs)
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()
        return Response(CourseCreateSerializers(new_course).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        user = self.request.user
        subscription = Subscription.objects.filter(user=user, course=course, is_active=True)
        if subscription:
            send_message_active(user.email, course.title)
        return Response(serializer.data)

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


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
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CoursesPaginator


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


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_sub = serializer.save()
        new_sub.user = self.request.user
        new_sub.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
