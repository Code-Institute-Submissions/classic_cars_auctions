from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    """Car model"""
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    firstRegistred = models.IntegerField()
    fuelType = models.CharField(max_length=50)
    odometer = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=50, null=True, blank=True)
    bodyType = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()
    reservedPrice = models.IntegerField()
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()

    def __str__(self):
        return str(self.make + " " + self.model)


class Bidder(models.Model):
    """Bidder Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)


class Bid(models.Model):
    """Bid Model"""
    car = models.ForeignKey('Car', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('Bidder', null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    winnerBid = models.BooleanField()
