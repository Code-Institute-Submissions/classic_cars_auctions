from django.shortcuts import render, get_object_or_404, redirect,reverse
from .models import Payment, PaymentLineItem
from auctions.models import Bid, Car


def payment(request, highest_bid_obj_id):
    """View to render Payment"""
    winner_bid = Bid.objects.filter(id=highest_bid_obj_id)
    if winner_bid[0].winnerBid and request.user.id == winner_bid[0].user_id:
        print(winner_bid[0].amount, winner_bid[0].time)
    else:
        return redirect(reverse('all_auctions'))

    print(request.user.id, winner_bid[0].user_id)
    
    context = {
        'winner_bid': winner_bid,
    }
    
    return render(request, 'payment/payment.html', context)
