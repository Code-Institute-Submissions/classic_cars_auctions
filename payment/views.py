from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from auctions.models import Bid
from .models import Payment, PaymentLineItem
from django.contrib import messages



@login_required()
def payment(request, highest_bid_obj_id):
    """View to render Payment"""
    winner_bid = Bid.objects.filter(id=highest_bid_obj_id)
    if winner_bid[0].winnerBid and request.user.id == winner_bid[0].user_id:
        print(winner_bid[0].amount, winner_bid[0].time)
    else:
        messages.error(request, 'Unauthorized Access.')
        return redirect(reverse('all_auctions'))
  
    context = {
        'winner_bid': winner_bid,
    }
    
    return render(request, 'payment/payment.html', context)
