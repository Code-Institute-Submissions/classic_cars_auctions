""" Auctions urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('all_auctions', views.all_auctions, name='all_auctions'),
    path('auction_detail/<int:car_id>/',
         views.auction_detail, name='auction_detail'),
    path('add/', views.add_auction, name='add_auction'),
    path('edit/<int:car_id>/',
         views.edit_auction, name='edit_auction'),
    path('delete/<int:car_id>/', views.delete_auction, name='delete_auction'),
]
