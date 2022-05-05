import uuid

from django.db import models

from auctions.models import Bid, Car


class Payment(models.Model):
    """Payment Model"""
    payment_number = models.CharField(max_length=32, null=False, 
                                      editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    deposit = models.IntegerField()


    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.payment_number:
            self.payment_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_number


class PaymentLineItem(models.Model):
    """paymentLineItem Model"""
    payment = models.ForeignKey(Payment, null=False, blank=False,
                                on_delete=models.CASCADE,
                                related_name='lineitems')
    car = models.ForeignKey(Car, null=False, blank=False,
                            on_delete=models.CASCADE)
    winner_bid = models.ForeignKey(Bid, null=False,
                            blank=False, on_delete=models.CASCADE)
    deposit = models.DecimalField(max_digits=6, decimal_places=2, null=False, 
                                  blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method 
        and update the deposit.
        """
        self.deposit = self.winner_bid.amount / 10
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.car.make} on order {self.payment.payment_number}'
