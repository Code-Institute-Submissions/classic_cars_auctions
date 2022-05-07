from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auctions.models import Bid

from .forms import PaymentForm


@login_required()
def payment(request, highest_bid_obj_id):
    """View to render Payment"""
    deposit = 0
    payment_form = PaymentForm()
    winner_bid = Bid.objects.filter(id=highest_bid_obj_id)
    if winner_bid[0].winnerBid and request.user.id == winner_bid[0].user_id:
        deposit = winner_bid[0].amount / 10
    else:
        messages.error(request, 'Unauthorized Access.')
        return redirect(reverse('all_auctions'))
   
    context = {
       'winner_bid': winner_bid,
       'payment_form': payment_form,
       'deposit': deposit,
    }
    
    return render(request, 'payment/payment.html', context)
