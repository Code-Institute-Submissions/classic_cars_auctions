""" Payment urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('<highest_bid_obj_id>', views.payment, name='payment')
]
