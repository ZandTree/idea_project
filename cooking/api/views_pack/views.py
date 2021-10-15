from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers.ideas.idea_ser import IdeaSerializer
from ideas.models import Category, Idea
from profiles.models import Profile

User = get_user_model()


class IdeasPerCategListView(generics.ListAPIView):
    """ retrieve all ideas linked to the category;
    for tests set pagination_class = None
    """
    serializer_class = IdeaSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        categ = get_object_or_404(Category, slug=slug)
        if categ.get_children():
            categ_descend = categ.get_descendants(include_self=True)
            qs = Idea.objects.filter(categ__in=categ_descend)
        else:
            qs = Idea.objects.filter(categ=categ)
        return qs


class TagIdeasListSlug(generics.ListAPIView):
    """ get list of ideas based on a tag's slug"""
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug is not None:
            return Idea.objects.filter(tags__slug__in=(slug,))
        else:
            return Response(status=400)


class IdeasFollowing(ListAPIView):
    """list of ideas (user is following): newest on top"""
    serializer_class = IdeaSerializer
    ordering_fields = ('title', 'created_at', 'max_rating')
    # default ordering
    ordering = ('-created_at',)

    def get_queryset(self):
        unid = self.kwargs.get('unid')
        person = get_object_or_404(Profile, unid=unid)
        person_following_list = person.following.values_list('id', flat=True)
        qs = Idea.objects.filter(author_id__in=person_following_list)
        return qs
