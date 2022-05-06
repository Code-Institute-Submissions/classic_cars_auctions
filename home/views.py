from django.shortcuts import render, get_object_or_404
from auctions.models import Bid, Car


def index(request):
    """ A view to return the index page """
    car = None
    highest_bid = 0
    highest_bid = Bid.objects.filter(winnerBid=True).last()

    if highest_bid:
        car_id = Bid.objects.filter(winnerBid=True).last().car.id
        highest_bid = Bid.objects.filter(winnerBid=True).last().amount
        car = get_object_or_404(Car, id=car_id)

    context = {
        'car': car,
        'highest_bid': highest_bid,
    }
    return render(request, 'home/index.html', context)
