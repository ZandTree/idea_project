from rest_framework import serializers as ser
from ideas.models import Category


# N1 for catges menu
# categories with children: for rendering in left side menu and indentation

class FilterCategListSerializer(ser.ListSerializer):
    """filter categs: front should get a list with only root categs"""

    def to_representation(self, objects):
        data = objects.filter(parent=None)
        return super().to_representation(data)


class CustomChildrenSerializer(ser.Serializer):
    """child should be serialized by CategorySer-er"""

    def to_representation(self, obj):
        serializer = self.parent.parent.__class__(obj)
        return serializer.data


class CategorySerializer(ser.ModelSerializer):
    """ list of categs with tree structure"""
    # each related object if parent has attr children == 'related name' from model FK
    #    and will be ser-ed by CategorySerializer; you need children (no need parents) """    
    children = CustomChildrenSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'children')
        # over-write list_ser_cls (to filter data: only parents)
        list_serializer_class = FilterCategListSerializer


# 2 for idea form
# list of all categories for drop-down: user to choose by creating a new idea
class CategoryNameSerializer(ser.ModelSerializer):
    """  list of categs without tree-structure"""

    class Meta:
        model = Category
        fields = ('name', 'id')
