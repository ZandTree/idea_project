from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from timestamp.broadcast_utils.base_utils import get_random_str
from timestamp.broadcast_utils.idea_utils import upload_img
from timestamp.broadcast_utils.validators import validate_size
from timestamp.models import TimeStamp

ALLOWED_EXTENTIONS = ('JPG', 'JPEG', 'PNG')

User = get_user_model()

import logging

logger = logging.getLogger('django')


class CategoryManager(models.Manager):
    pass


class Category(MPTTModel):
    name = models.CharField(max_length=120, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            db_index=True,
                            related_name='children'
                            )
    objects = CategoryManager()

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class IdeaManager(models.Manager):
    pass


PROGR = 0
REVIEW = 1
PUB = 3


class Idea(TimeStamp):
    """
    tree cached fields: max_rating, avg_rate, an_likes will be calculated  only if attr's like or attr rating get updated
    via through model UserIdeaRelation
    """
    STATUS_CHOICES = (
        (PROGR, 'in progres'),
        (REVIEW, 'in review'),
        (PUB, 'published')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    categ = TreeForeignKey(Category,
                           related_name='ideas',
                           on_delete=models.PROTECT,
                           )
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    lead_text = models.CharField(max_length=254, default="")
    main_text = models.TextField()
    view_count = models.IntegerField(blank=True, default=0)
    thumbnail = models.ImageField(blank=True, null=True, upload_to=upload_img,
                                  validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENTIONS),
                                  validate_size])

    featured = models.BooleanField(blank=True, default=False)
    fans = models.ManyToManyField(User, related_name='idea_fans', through='UserIdeaRelation')
    is_public = models.BooleanField(default=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    tags = TaggableManager(blank=True, verbose_name="Tags", help_text="Tags should be separated by comma")
    avg_rate = models.DecimalField(decimal_places=2, max_digits=5, default=None, null=True)
    an_likes = models.IntegerField(default=None, null=True)
    max_rating = models.DecimalField( default=None, null=True,decimal_places=2, max_digits=5,)
    remove_file = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=5,null=True, blank=True,default="0.00")


    objects = IdeaManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        add attr slug to idea object if it was formed without slug 
        """
        start_creating = not self.pk
        if start_creating:
            try:
                super().save(*args, **kwargs)
                if not self.slug:
                    self.slug = get_random_str(10)
                    self.save()
            except Exception as e:
                logger.warning(f'Failed creating idea with exception {e}')
            else:
                logger.info(f'Idea object created id: {self.id}')
            finally:
                pass
        else:
            super().save(*args, **kwargs)


class UserIdeaRelation(models.Model):
    """ if attr rating or like get updated cached fields in idea model will be also re-calculated """
    RATING = (
        (1, 'OK'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Excellent')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    like = models.BooleanField(blank=True, default=False)
    dislike = models.BooleanField(blank=True, default=False)
    in_bookmark = models.BooleanField(blank=True, default=False)
    rating = models.PositiveSmallIntegerField(choices=RATING, null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_rating = self.rating
        self.old_like = self.like

    def __str__(self):
        return f'User: {self.user} active in user-idea-relations {self.like}, {self.rating}'

    def save(self, *args, **kwargs):
        """ import here: to avoid circular import (idea-user-relation calls idea-user-relation)"""
        from .logic import calc_count_likes, calc_max_rating, calc_rating

        # if like or rating changed |=> re-calc total likes on idea
        start_creating = not self.pk
        super().save(*args, **kwargs)  # here idea gets (if triggered by change rating event)
        new_rating = self.rating
        new_like = self.like

        if self.old_rating != new_rating or start_creating:
            # obj is already exist,so working on condition old != new
            calc_rating(self.idea)
            calc_max_rating(self.idea)

        if self.old_like != new_like or start_creating:
            # user-idea-rel obj is just created            
            calc_count_likes(self.idea)
