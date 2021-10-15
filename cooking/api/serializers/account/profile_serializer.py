from django.contrib.auth import get_user_model
from rest_framework import serializers as ser

from profiles.models import Profile
from api.serializers.account.user_serializer import UserSerializer
from timestamp.broadcast_utils.validators import validate_size

User = get_user_model()

import logging

logger = logging.getLogger('upload')


class ProfileSerializer(ser.ModelSerializer):
    """ serve crud operations on profile(via form) """
    user = UserSerializer(many=False, read_only=True)
    name = ser.ReadOnlyField(source='get_name')
    website = ser.URLField(required=False)
    image = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    # let op: without allow_null = can't remove file from form and send to backend
    # to learn: image = serializers.ImageField(max_length=None, use_url=True)
    followers = ser.SerializerMethodField()
    count_followers = ser.SerializerMethodField()

    following = ser.SerializerMethodField()
    count_following = ser.SerializerMethodField()  # via annotated qs in view

    class Meta:
        model = Profile
        fields = ('bio', 'website', 'unid', 'image', 'name', 'following', 'user', 'followers', 'count_following',
                  'count_followers', 'remove_file')

    def save(self, *args, **kwargs):
        print("in ser-er")
        print(self.validated_data)
        del_previous_file = self.validated_data.get('remove_file')
        img = self.validated_data.get('image', None)

        try:
            if self.instance.pk and del_previous_file:
                # if self.instance.pk and img is not None:
                # need for deleting url in db but also on aws3   
                self.instance.image.delete()
            if self.instance.pk and img is None and del_previous_file:
                self.instance.image.delete()

        except ValueError as e:
            logger.warning(f'Value err in profile ser-er {e}')

        except TypeError as e:
            logger.warning(f'Type error in profile ser-er {e}')

        except Exception as e:
            logger.warning(f'General exception in profile ser-er {e}')

        finally:
            pass
        super().save(*args, **kwargs)

    def get_following(self, obj):
        """qs of users """
        try:
            qs = obj.following.all()
            if qs.count() > 0:
                data = [{'unid': user.profile.unid, 'user_id': user.id, 'username': user.username, 'id': user.id} for
                        user in qs]
            else:
                data = []
            return data
        except Profile.DoesNotExist:
            raise ser.ValidationError("Profile  does not exist")

    def get_count_following(self, obj):
        return obj.following.count()

    def get_followers(self, obj):
        """ qs of profiles(check)?"""
        qs = obj.user.followed_by.all()
        if qs.count() > 0:
            data = [{'unid': obj.unid, 'user_id': obj.id, 'username': obj.user.username, 'id': obj.user.id} for obj in
                    qs]
        else:
            data = []
        return data

    def get_count_followers(self, obj):
        """qs of profiles"""
        count = obj.user.followed_by.count()
        return count
