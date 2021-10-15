from django.contrib import admin
from comments.models import Comment
from mptt.admin import MPTTModelAdmin


class CommentAdmin(MPTTModelAdmin):
    mptt_indent_field = "id"
    mptt_level_indent = 20
    list_display = ('id', 'user', 'idea', 'reply_to', 'body')


admin.site.register(Comment, CommentAdmin)
