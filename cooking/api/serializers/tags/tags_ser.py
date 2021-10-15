from rest_framework import serializers as ser

from taggit.models import Tag


class TagSerializer(ser.ModelSerializer):
    id = ser.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'slug', 'name',)
