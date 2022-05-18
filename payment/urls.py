""" Payment urls
"""
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.get_payment, name='get_payment'),
    path('payment_success/<payment_number>',
         views.payment_success, name='payment_success'),
    path('cache_payment_data/', views.cache_payment_data, name='cache_payment_data'),
    path('wh/', webhook, name='webhook'),

]
