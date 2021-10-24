from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSer
from rest_framework import serializers as ser

User = get_user_model()


class UserSerializer(DjoserUserSer):
    """inside UserSerializer inherited from djoser"""
    unid = ser.CharField(source='profile.unid', read_only=True)
    username = ser.CharField(read_only=True)

    class Meta(DjoserUserSer.Meta):
        model = User
        fields = ('id', 'username', 'unid')
