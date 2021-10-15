from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers as ser
from comments.models import Comment

User = get_user_model()


class CommentSerializer(ser.ModelSerializer):
    """ serializer for creating-editing-deleting a comment"""
    author_comment = ser.CharField(source='user.username', read_only=True)
    name_recepient = ser.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'body', 'idea_id',
                  'user_id', 'reply_to_id', 'parent', 'author_comment', 'deleted', 'name_recepient'

                  )

    def get_name_recepient(self, obj):
        """return username of the user who got a reply"""
        try:
            if obj.parent is not None:
                return get_object_or_404(User, id=obj.reply_to_id).username
        except:
            return None
        finally:
            pass
