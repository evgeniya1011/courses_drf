from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
