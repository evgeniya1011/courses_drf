from rest_framework import serializers

from courses.models import Course, Lesson, Payments


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializers(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        return instance.lesson.all().count()


class CourseCreateSerializers(serializers.ModelSerializer):
    lesson = LessonSerializers(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        lesson = validated_data.pop('lesson')
        course = Course.objects.create(**validated_data)
        for les in lesson:
            Lesson.objects.create(course=course, **les)
        return course


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
