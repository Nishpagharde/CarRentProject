from django.core.validators import *
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    password=models.CharField(max_length=80)
    def __str__(self):
        return self.name


class Car(models.Model):
    vehicle_number = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    rent_per_day = models.IntegerField()
    availability = models.BooleanField(null=True)

    def __str__(self):
        return self.model


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return str(self.customer) + "- " + str(self.car)

class CarDealer(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.CharField(max_length=30)
    email= models.EmailField(max_length=30)

    def __str__(self):
        return self.name