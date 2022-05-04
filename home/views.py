from django.shortcuts import render, get_object_or_404
from auctions.models import Bid, Car


def index(request):
    """ A view to return the index page """
    highest_bid = Bid.objects.filter(winnerBid=True).last().amount
    highest_bid_id = Bid.objects.filter(winnerBid=True).last().car.id
    print(highest_bid_id)
 
    if highest_bid:
        car = get_object_or_404(Car, id=highest_bid_id)

    context = {
        'car': car,
        'highest_bid': highest_bid,
    }
    return render(request, 'home/index.html', context)
