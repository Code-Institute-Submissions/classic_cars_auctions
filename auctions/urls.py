""" Auctions urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('all_auctions', views.all_auctions, name='all_auctions'),
    path('auction_detail/<car_id>',
         views.auction_detail, name='auction_detail'),
    path('get_user_bid', views.get_user_bid, name='get_user_bid'),
]
