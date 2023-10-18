from django.shortcuts import render
from rest_framework import viewsets, generics

from courses.models import Course, Lesson
from courses.serializers import CourseSerializers, LessonSerializers


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()


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




