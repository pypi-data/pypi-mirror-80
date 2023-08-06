from django.contrib.auth.models import Permission, Group, User
from rest_framework import viewsets

from django_boilerplate_rest.serializers import PermissionSerializer, GroupSerializer, UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
