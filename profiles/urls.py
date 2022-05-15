from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('payment_history/<payment_number>', views.payment_history, name='payment_history'),

]
