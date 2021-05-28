from django.core.exceptions import ValidationError

def validate_number(value):
    try:
        num = int(value)
    except Exception:
        raise ValidationError(f"{value} is not a valid phone number")