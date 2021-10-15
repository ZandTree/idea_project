from django.core.exceptions import ValidationError


def validate_size(value):
    """ check if uploaded file is too large"""
    # print("validator size inside model field")
    filesize = value.size
    # if filesize > 24:# for testing
    if filesize > 250000:
        raise ValidationError("File is too large; should be less then 2MB")
    return value
