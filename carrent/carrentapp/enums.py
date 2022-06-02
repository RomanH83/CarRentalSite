from django.db import models


# Choices for Car model fields
class CarEngineType(models.TextChoices):
    BENZYNOWY = 'PE', "Benzynowy"
    DIESEL = 'DI', "Diesel"
    ELEKTRYCZNY = 'EL', "Elektryczny"
    HYBRYDA = 'HY', "Hybryda"

class CarGearboxType(models.TextChoices):
    AUTOMATYCZNA = 'A', "Automatyczna"
    MANUALNA = 'M', "Manualna"

# Choices for Order model fields
class OrderStatus(models.TextChoices):
    AKTYWNY = 'A', 'Aktywny'
    HISTORIA = 'H', 'Historia'

