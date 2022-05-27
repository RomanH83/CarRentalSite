from django.core.exceptions import ValidationError

from carrentapp.validators import catch_validation_error


@catch_validation_error
def new_mileage_validator(new_mileage, old_mileage):
    """
    Function takes 2 integers and checks if staff input is correct
    """
    if old_mileage > new_mileage:
        raise ValidationError("Nowy przebieg nie może być mniejszy niż stary")
