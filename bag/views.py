from django.shortcuts import render
from auctions.models import Bid, Car, Bidder


def view_bag(request):
    """View to display auctions that the user won """
    if request.user.is_authenticated:
        user_id = request.user.id
    
    

    return render(request, 'bag/view_bag.html')
