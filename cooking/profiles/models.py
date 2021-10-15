from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from timestamp.models import TimeStamp
from timestamp.broadcast_utils.idea_utils import upload_img
from timestamp.broadcast_utils.validators import validate_size

ALLOWED_EXTENTIONS = ('JPG', 'JPEG', 'PNG')

User = get_user_model()


class Profile(TimeStamp):
    """ badge_bg (creat random bg-color by creating profile object; optional)"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    unid = models.CharField(max_length=6, blank=True, db_index=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_img,
                              validators=[FileExtensionValidator(ALLOWED_EXTENTIONS), validate_size])
    bio = models.TextField(blank=True, default="")
    website = models.URLField(max_length=100, default="", blank=True)
    badge_bg = models.CharField(max_length=30, default="", blank=True)
    following = models.ManyToManyField(User, related_name="followed_by", blank=True)
    remove_file = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    def get_name(self):
        return self.user.username
