from django.shortcuts import render
from .models import Car


def all_cars(request):
    """ A view to return all cars and for sorting cars """
    cars = Car.objects.all()
    context = {
        'cars': cars,
    }
    return render(request, 'auctions/cars.html', context)
