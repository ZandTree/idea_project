from django.db.models.signals import pre_save
from django.dispatch import receiver
from timestamp.broadcast_utils.base_utils import make_slug

from ideas.models import Idea


@receiver(pre_save, sender=Idea)
def idea_presave_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = make_slug(instance)
