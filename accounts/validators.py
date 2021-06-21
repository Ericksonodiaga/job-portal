import os
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    value = str(value)
    if not (value.startswith("+2547") or value.startswith("+2541")):
        raise ValidationError("Phone number must start with +2547XXX, or +2541XXX")

    if not len(value) == 13:
        raise ValidationError("Phone number is incorrect Length")


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Incorrect file Extensions: supported extensions{valid_extensions}')
