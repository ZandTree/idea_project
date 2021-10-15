from django.db import models


class TimeStamp(models.Model):
    '''it is abstract so no db table'''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
