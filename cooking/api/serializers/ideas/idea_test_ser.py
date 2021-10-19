from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers as ser
# help module for taggit
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from ideas.models import Idea


User = get_user_model()


class IdeaTestSerializer(TaggitSerializer, ser.ModelSerializer):

    categ_name = ser.ReadOnlyField(source='categ.name')

    """ ONLY FOR TESTING:excl created_at: for testing """    
    owner_idea = ser.CharField(source='author.username', default="", read_only=True)    
    author = ser.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                        default=ser.CurrentUserDefault()
                                        )
    categ_name = ser.ReadOnlyField(source='categ.name')
    tags = TagListSerializerField(required=False)
    
    class Meta:
        model = Idea

        fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug',
                  'owner_idea', 'categ_name', 'categ', 'status', 'an_likes', 'avg_rate', 'featured', 'tags', )
        

        fields = (
            'id', 'slug', 'title', 'author', 'lead_text', 'main_text', 'owner_idea', 'categ_name', 'categ', 'status', 'an_likes', 'avg_rate', 'featured', 'tags', 

        )

    