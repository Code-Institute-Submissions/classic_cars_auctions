from django_countries.fields import CountryField

from django.db import models
from auctions.models import Bid, Car
from profiles.models import UserProfile


class Payment(models.Model):
    """Payment Model"""
    payment_number = models.CharField(max_length=32, null=False,
                                      editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='payment')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='car')
    bids = models.ForeignKey(Bid, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='Bid')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

