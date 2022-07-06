from datetime import date

from django.db import models

from accounts.models import UserCustom
from carrentapp.enums import CarEngineType, CarGearboxType, OrderStatus
from carrentapp.utilities import calculate_cost


class CarBrand(models.Model):
    brand_name = models.CharField(max_length=50, verbose_name="Marka", unique=True)

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Marki"

    def __str__(self):
        return f'{self.brand_name}'


class CarModel(models.Model):
    model_name = models.CharField(max_length=50, verbose_name="Model")
    brand = models.ForeignKey(CarBrand, verbose_name="Marka", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Modele"

    def __str__(self):
        return f'{self.model_name}'


class Car(models.Model):
    plate_number = models.CharField(max_length=20, verbose_name="Numer rejestracyjny", unique=True)
    brand = models.ForeignKey(CarBrand, verbose_name="Marka", on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModel, verbose_name="Model", on_delete=models.PROTECT)

    year_of_production = models.IntegerField(verbose_name="Rok produkcji")
    rating = models.FloatField(verbose_name="Ocena")
    number_of_seats = models.IntegerField(verbose_name="Ilość miejsc")
    engine_type = models.CharField(max_length=2, verbose_name="Rodzaj silnika",
                                   choices=CarEngineType.choices)
    engine_power = models.IntegerField(verbose_name="Moc")
    color = models.CharField(max_length=20, verbose_name="Kolor")
    car_mileage = models.IntegerField(verbose_name="Przebieg")
    car_image = models.ImageField(upload_to='images/cars', verbose_name="Zdjęcie")
    gearbox_type = models.CharField(max_length=1, verbose_name="Skrzynia biegów", choices=CarGearboxType.choices)

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"

    def __str__(self):
        return f'{self.plate_number} - {self.brand} {self.car_model}'


class BasePrice(models.Model):
    base_price = models.IntegerField(verbose_name="Cena Bazowa")

    class Meta:
        verbose_name = "Cena Bazowa"
        verbose_name_plural = "Cena Bazowa"

    def __str__(self):
        return f'Cena Bazowa: {self.base_price}'


class Order(models.Model):
    client = models.ForeignKey(UserCustom, verbose_name="Klient", on_delete=models.PROTECT)
    car = models.ForeignKey(Car, verbose_name="Samochód", on_delete=models.PROTECT)
    base_price = models.ForeignKey(BasePrice, verbose_name="Cena bazowa", on_delete=models.PROTECT)

    rent_cost = models.IntegerField(verbose_name="Koszt wynajmu", blank=True, null=True)
    start_date = models.DateField(verbose_name="Start")
    return_date = models.DateField(verbose_name="Zwrot")
    order_length = models.IntegerField(verbose_name="Długość wypożyczenia", default=0)
    kilometers_traveled = models.IntegerField(verbose_name="Przejechane kilometry", default=0)
    order_datetime = models.DateTimeField(verbose_name="Powstanie zamówienia", auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Edytowane", auto_now=True)

    status = models.CharField(max_length=1,
                              verbose_name="Status",
                              choices=OrderStatus.choices,
                              default=OrderStatus.AKTYWNY)
    issue_resolved = models.BooleanField(verbose_name="Problem rozwiązany", null=True)

    class Meta:
        verbose_name = "Log Wypozyczenia"
        verbose_name_plural = "Logi Wypozyczen"

    def __str__(self):
        return f'{self.client.email} {self.car.plate_number} =>ID {self.id}'

    @property
    def cost_calculator(self):
        base_price = self.base_price.base_price
        car_rating = self.car.rating
        time_discount = TimeDiscount.objects.last()
        car_discount_obj = BrandDiscount.objects.last()
        if car_discount_obj.car_brand == self.car.brand:
            car_discount = car_discount_obj.brand_discount
        else:
            car_discount = 0
        user_discount = self.client.get_user_discount
        cost = calculate_cost(self.start_date,
                              self.return_date,
                              base_price,
                              car_rating, user_discount, time_discount, car_discount)
        return cost

    @property
    def is_future(self):
        if self.start_date > date.today():
            return True
        else:
            return False

    @property
    def is_past(self):
        if self.return_date < date.today():
            return True
        else:
            return False

    def save(self, *args, **kwarg):
        self.rent_cost = self.cost_calculator
        self.order_length = (self.return_date - self.start_date).days
        super(Order, self).save(*args, **kwarg)


class TimeDiscount(models.Model):
    month_discount = models.IntegerField(verbose_name="Zniżka miesięczna")
    two_weeks_discount = models.IntegerField(verbose_name="Zniżka dwutygodniowa")


class BrandDiscount(models.Model):
    car_brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, null=True)
    brand_discount = models.IntegerField(verbose_name="Zniżka na marke")


class BaseUserDiscount(models.Model):
    max_discount = models.IntegerField(verbose_name="Maksymalna zniżka")
    increment_per_tick = models.IntegerField(verbose_name="Skok zniżki")
    orders_per_tick = models.IntegerField(verbose_name="Co ile zamówień skok")
    min_order_length = models.IntegerField(verbose_name="Minimalna długość zamówienia")
