from rest_framework import serializers

from courses.models import Course, Lesson, Payments


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializers(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instanse):
        return instanse.lesson_set.all().count()

    def create(self, validated_data):
        lessons_data = validated_data.pop('lesson')
        course = Course.objects.create(**validated_data)
        if lessons_data:
            for lesson_data in lessons_data:
                Lesson.objects.create(course=course, **lesson_data)
        return course


# class CourseCreateSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = '__all__'
#
#     def create(self, validated_data):
#         lessons_data = validated_data.pop('lesson')
#         course = Course.objects.create(**validated_data)
#         if lessons_data:
#             for lesson_data in lessons_data:
#                 Lesson.objects.create(course=course, **lesson_data)
#         return course


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'



