""" Auctions urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('auctions', views.all_cars, name='cars'),
]
