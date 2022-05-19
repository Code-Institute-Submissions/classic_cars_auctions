from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from auctions.models import Bid, Car
from .models import Payment
from .forms import PaymentForm

import stripe
import json


@require_POST
def cache_payment_data(request):
    """Cach Payment"""
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'payment_info': json.dumps(request.session.get(
                                       'payment_info', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required()
def get_payment(request):
    """View to render Payment"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    payment_info = request.session.get('payment_info', {})
    user_id = request.user.id

    user_id = request.user.id
    for item in payment_info:
        car_id = item['car_id']
        winner_bid_id = item['winner_bid_id']

        winner_bid = Bid.objects.get(id=winner_bid_id)
        car = Car.objects.get(id=car_id)
        car_price = winner_bid.amount
        payment_amount = car_price / 10

    if request.method == 'POST':
        payment_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        payment_form = PaymentForm(payment_data)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.car = car
            payment.bids = winner_bid
            payment.deposit = payment_amount
            payment.save()

            if payment:
                request.session['save_info'] = 'save_info' in request.POST
                return redirect(reverse('payment_success',
                                args=[payment.payment_number]))
            else:
                messages.error(request, 'try agin')
                return redirect(reverse('get_payment'))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        payment_info = request.session.get('payment_info', {})
        if not payment_info:
            return redirect(reverse('all_auctions'))

        stripe_total = round(payment_amount * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                payment_form = PaymentForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                payment_form = PaymentForm()
        else:
            payment_form = PaymentForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    print(payment_amount)
    context = {
        'payment_form': payment_form,
        'car_price': car_price,
        'payment_amount': payment_amount,
        'winner_bid': winner_bid,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'payment/payment.html', context)


def payment_success(request, payment_number):
    """
    Handle successful payment
    """
    save_info = request.session.get('save_info')
    payment = get_object_or_404(Payment, payment_number=payment_number)

    left_to_pay = payment.bids.amount - payment.bids.amount / 10
    print(left_to_pay)

    profile = UserProfile.objects.get(user=request.user)
    # Attach the user's profile to the Payment
    payment.user_profile = profile
    payment.save()

    # Save the user's info
    if save_info:
        profile_data = {
            'default_phone_number': payment.phone_number,
            'default_country': payment.country,
            'default_postcode': payment.postcode,
            'default_town_or_city': payment.town_or_city,
            'default_street_address1': payment.street_address1,
            'default_street_address2': payment.street_address2,
            'default_county': payment.county,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f'Payment successfully processed! \
        Your Payment number is { payment_number }. A confirmation \
        email will be sent to { payment.email }.')

    if 'payment_info' in request.session:
        del request.session['payment_info']

    template = 'payment/payment_success.html'
    context = {
        'payment': payment,
        'left_to_pay': left_to_pay,

    }

    return render(request, template, context)
