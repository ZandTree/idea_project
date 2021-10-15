from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from ideas.models import Idea
from timestamp.models import TimeStamp

User = get_user_model()


class CommentManager(models.Manager):
    # even if it's empty <class 'mptt.querysets.TreeQuerySet'>|=> queryset
    pass


class Comment(TimeStamp, MPTTModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=6548)
    # tree structure
    parent = TreeForeignKey("self",
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            related_name="children"
                            )
    # id replied person
    reply_to = models.ForeignKey(User,
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE,
                                 related_name='reply_ers'
                                 )

    banned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    deleted_content = models.TextField(default="", blank=True)
    objects = CommentManager()  # even if it's empty <class 'mptt.querysets.TreeQuerySet'>|=> queryset

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.body[:5]
