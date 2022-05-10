""" Payment urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_payment, name='get_payment'),
    path('payment_success/<payment_number>', views.payment_success, name='payment_success'),
]
