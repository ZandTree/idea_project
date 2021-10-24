import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from timestamp.broadcast_utils.base_utils import create_color, make_unid

from profiles.models import Profile

logger = logging.getLogger('user_issues')
User = get_user_model()


@receiver(post_delete, sender=Profile)
def auto_delete_user(sender, instance, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        print('user does not exist')
    else:
        instance.user.delete()


# user created |==> create his profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    """create_or_update profile"""
    try:
        if created and instance.email:
            Profile.objects.create(user=instance)
            logger.info(f'profile created for {instance.email}')
    except:
        logger.error('profile creation failed')
    finally:
        pass

    # before profile get saved in db |==> create unid,displayname,random bg color for avatar


@receiver(pre_save, sender=Profile)
def add_unid(sender, instance, **kwargs):
    if not instance.unid:
        instance.unid = make_unid(instance)

