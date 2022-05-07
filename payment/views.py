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
       'stripe_public_key': 'pk_test_51KgHIsA2xS5xmfsxSeIRUuMEGtdvUMiDOu6i20EFqkp5s9gcR0WGDQMhWwrbAqMa3oV8hF52GTD5HsRqyVUY7dt200R7AllYsj',
       'client_secret': 'test client secret',
    }

    return render(request, 'payment/payment.html', context)
