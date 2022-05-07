from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

import stripe

from auctions.models import Bid
from .forms import PaymentForm


@login_required()
def payment(request, highest_bid_obj_id):
    """View to render Payment"""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    deposit = 0
    payment_form = PaymentForm()
    winner_bid = Bid.objects.filter(id=highest_bid_obj_id)
    if not (winner_bid[0].winnerBid and 
           (request.user.id == winner_bid[0].user_id)):
        messages.error(request, 'Unauthorized Access.')
        return redirect(reverse('all_auctions'))

    deposit = winner_bid[0].amount / 10
    stripe_total = round(deposit * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing')
    context = {
       'winner_bid': winner_bid,
       'payment_form': payment_form,
       'deposit': deposit,
       'stripe_public_key': stripe_public_key,
       'client_secret': intent.client_secret,
    }

    return render(request, 'payment/payment.html', context)
