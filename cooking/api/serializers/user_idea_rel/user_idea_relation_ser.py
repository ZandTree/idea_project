from django.contrib.auth import get_user_model
from rest_framework import serializers as ser
from ideas.models import UserIdeaRelation

User = get_user_model()


class UserIdeaRelSerializer(ser.ModelSerializer):
    """ custom attr to display add/remove likes """

    class Meta:
        model = UserIdeaRelation
        fields = (
            'like', 'rating'
        )
