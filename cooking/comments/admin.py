from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from comments.models import Comment


class CommentAdmin(MPTTModelAdmin):
    mptt_indent_field = "id"
    mptt_level_indent = 20
    list_display = ('id', 'user', 'idea', 'reply_to', 'body')


admin.site.register(Comment, CommentAdmin)
