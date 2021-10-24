import random
import string

from django.utils.text import slugify


def get_random_str(size):
    """create random string from letters and digits"""
    chars = string.ascii_letters + string.digits
    final_str = [random.choice(chars) for _ in range(size)]
    return "".join(final_str)


def get_random_num(size):
    """create random string from letters and digits"""
    chars = string.digits
    final_digits = [random.choice(chars) for _ in range(size)]
    return "".join(final_digits)


def make_unid(instance, size=5):
    """
    create unique id for instance based on random letters and digits
    which have attr = uid
    """
    klass = instance.__class__
    start_unid = get_random_str(size)
    if klass.objects.filter(unid=start_unid).exists():
        instance.unid = get_random_str(size)
        return make_unid(instance)
    return start_unid


def make_slug(instance, new_slug=None):
    """
    instance of model with slug attr and char(title)
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exist = Klass.objects.filter(slug=slug).exists()
    if qs_exist:
        extra = get_random_str(4)
        new_slug = f"{slug}-{extra}"
        return make_slug(instance, new_slug=new_slug)
    return slug


def make_unique_slug(instance, size=6):
    """create unique slug based on random digits and letters"""
    Klass = instance.__class__
    slug_ = get_random_str(size)
    qs_exist = Klass.objects.filter(slug=slug_).exists()
    if qs_exist:
        instance.slug = get_random_str(size)
        return make_unique_slug(size)
    return slug_


def create_color():
    red = random.randint(0, 266)
    green = random.randint(0, 266)
    blue = random.randint(0, 266)
    return f'({red},{green},{blue})'
