from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Car



def all_auctions(request):
    """ A view to return all cars and for sorting cars """

    cars = Car.objects.all()
    filter = Car


    context = {
        'cars': cars,
    }

    return render(request, 'auctions/auctions.html', context)


def auction_detail(request, car_id):
    """ A view to return car and auctions detail """
    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }

    return render(request, 'auctions/auction_detail.html', context)
