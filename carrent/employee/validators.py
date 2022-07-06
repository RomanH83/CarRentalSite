from django.core.exceptions import ValidationError

from carrentapp.validators import catch_validation_error
from carrentapp.enums import OrderStatus


@catch_validation_error
def new_mileage_validator(new_mileage, old_mileage):
    """
    Function takes 2 integers and checks if staff input is correct
    """
    if old_mileage > new_mileage:
        raise ValidationError("Nowy przebieg nie może być mniejszy niż stary")

@catch_validation_error
def status_check(status):
    """
    Function takes a string as status and checks if it matches required status
    It is used to prevent changing car mileage without ending an order
    """
    if status != OrderStatus.HISTORIA:
        raise ValidationError("Jeśli wprowadzasz nowy przebieg, status musisz zmienić na Historia")

