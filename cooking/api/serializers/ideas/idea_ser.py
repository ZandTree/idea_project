from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers as ser
# help module for taggit
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from ideas.models import Idea
from timestamp.broadcast_utils.validators import validate_size

import logging

logger = logging.getLogger('upload')

User = get_user_model()


class IdeaSerializer(TaggitSerializer, ser.ModelSerializer):
    categ_name = ser.ReadOnlyField(source='categ.name')
    author_unid = ser.ReadOnlyField(source='author.unid', read_only=True)
    owner_idea = ser.CharField(source='author.username', default="", read_only=True)
    author = ser.PrimaryKeyRelatedField(queryset=User.objects.all(), default=ser.CurrentUserDefault())
    tags = TagListSerializerField(required=False)
    users_comments = ser.IntegerField(read_only=True)
    thumbnail = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
        
    class Meta:
        model = Idea
        fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug','users_comments',
                  'owner_idea', 'author_unid', 'categ_name', 'categ', 'created_at', 'status', 'thumbnail',
                  'avg_rate', 'an_likes', 'featured', 'tags', 'max_rating',  'remove_file')

    def save(self, *args, **kwargs):
        """ if idea has already thumbnail it will be replaced by a new img
        otherwise thumbnail attr gets a value(new img)
        # no img from front( img not attached (empty str) or not changed (str = url aws s3))
        validated data: 'thumbnail', None / 'remove_file', False
        # user attached img: 
        validated data: ('thumbnail', <InMemoryUploadedFile: one.jpg (image/jpeg)>) 
        'remove_file' set to True in view and passed here       
        """
        del_previous_file = self.validated_data.get('remove_file')
        img = self.validated_data.get('thumbnail', None)
        # empty str in req.data |=> thumbnail == None
        # string aws s3 url     |=> thumbnail = None
        try:
            if self.instance.pk and img is None and del_previous_file:
                """
                case: user removes prev image and sends empty str as thumbnail back;
                    old img should be deleted on aws s3
                """
                self.instance.thumbnail.delete()
                logger.warning(f'user {self.instance.author} deleted img ')
            elif self.instance.pk and del_previous_file:
                """
                cases: 
                    1. prev file existes and get replaced (prevent formation of  orphan images on aws s3)
                    2. prev file doesn't exist and a new file comes                 
                without this block: new img will be linked with current idea but the old one with persist on aws3;
                """
                self.instance.thumbnail.delete()
                logger.warning(f'user {self.instance.author} deleted img from aws (and replaced it with a new one)')
        except Exception as e:
            # ignore: exception obj is just created and has no pk yet
            logger.warning(f'General exception in idea ser-er {e}')

        finally:
            pass
        super().save(*args, **kwargs)
