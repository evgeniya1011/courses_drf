from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsUserProfile
from users.serializers import UserSerializers, UserListSerializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsUserProfile]

    def get_object(self):
        return self.request.user


class UserProfileListView(generics.ListAPIView):
    serializer_class = UserListSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

