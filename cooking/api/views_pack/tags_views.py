from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from taggit.models import Tag
from api.serializers.tags.tags_ser import TagSerializer
from api.serializers.ideas.idea_ser import IdeaSerializer
from ideas.models import Idea

User = get_user_model()


class TagList(generics.ListAPIView):
    """ get list of tags"""
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_queryset(self, queryset=None):
        return Tag.objects.all()


class TagIdeasListName(generics.ListAPIView):
    """ get list of tags via names"""
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        name = self.kwargs.get('name')
        if name is not None:
            return Idea.objects.filter(tags__name__in=(name,))
        else:
            return Response(status=400)
