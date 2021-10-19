from django.db.models import Avg, Count, Case, When, Max
from .models import UserIdeaRelation
from decimal import Decimal


def calc_rating(obj):
    rating_val = UserIdeaRelation.objects.filter(idea=obj).aggregate(rate_value=(Avg('rating')))
    obj.avg_rate = rating_val.get('rate_value', None)
    obj.save()


def calc_count_likes(obj):
    agr_likes = UserIdeaRelation.objects.filter(idea=obj).aggregate(like_total=(Count(Case(When(like=True, then=1)))))
    obj.an_likes = agr_likes.get('like_total', None)
    obj.save()

    
def calc_max_rating(obj):
    max_rate = UserIdeaRelation.objects.filter(idea=obj).aggregate(max_rating=Max('rating'))    
    obj.max_rating = Decimal(max_rate.get('max_rating', None))    
    obj.save()
