from rest_framework import serializers

from courses.serializers import PaymentsSerializer
from users.models import User


class UserSerializers(serializers.ModelSerializer):
    payment = PaymentsSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = '__all__'
