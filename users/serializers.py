from rest_framework import serializers

from courses.serializers import PaymentsSerializer
from users.models import User


class UserSerializers(serializers.ModelSerializer):
    payment = PaymentsSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_name',)
