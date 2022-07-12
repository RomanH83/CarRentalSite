from datetime import date

from django.core.exceptions import ValidationError


def validation_age(birthdate):
    date_today = date.today()
    year = date_today.year
    min_birthday = date_today.replace(year=year - 18)
    if min_birthday < birthdate < date_today:
        raise ValidationError("Niestety nie jesteś pełnoletni/nia i nie możesz skorzystać z naszych usług")
    elif birthdate > date_today:
        raise ValidationError("Nieprawidłowa data urodzenia")

