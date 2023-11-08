from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, Lesson, Payments, Subscription
from courses.paginators import CoursesPaginator
from courses.serializers import CourseSerializers, LessonSerializers, PaymentsSerializer, CourseCreateSerializers, \
    SubscriptionSerializer
from courses.services import send_message_active
from users.permissions import IsModerator, IsNotModerator, IsOwner
import stripe


class CourseViewSet(viewsets.ModelViewSet):
    """ Создание, просмотр, обновление и удаление курса"""
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
    """Создание урока"""
    serializer_class = LessonSerializers
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveView(generics.RetrieveAPIView):
    """ Просмотр информации по уроку"""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    """ Обновление урока"""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonListView(generics.ListAPIView):
    """ Просмотр всех уроков"""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CoursesPaginator


class LessonDestroyView(generics.DestroyAPIView):
    """ Удаление урока """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator | IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    """ Просмотр всех платежей"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('date_payment',)


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.save()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        starter_subscription = stripe.Product.create(
            name=new_payment.course.title,
            description=new_payment.course.description,
        )

        starter_subscription_price = stripe.Price.create(
            unit_amount=new_payment.amount,
            currency="rub",
            recurring={"interval": "month"},
            product=starter_subscription['id'],
        )

        payment_session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/success",
            cancel_url="http://127.0.0.1:8000/cancel",
            line_items=[
                {
                    "price": starter_subscription_price.id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
        )
        return Response(payment_session)


class PaymentsRetrieveAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def get(self, request, payment_id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment = stripe.checkout.Session.retrieve(payment_id)
        detail_payment = {
            'status': payment['payment_status']
        }
        return Response(detail_payment)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Создание подписки """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_sub = serializer.save()
        new_sub.user = self.request.user
        new_sub.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Удаление подписки """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
