from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(val):
    current_year = timezone.now().year
    if val > current_year:
        raise ValidationError(
            'Год должен быть меньше или равен текущему')
