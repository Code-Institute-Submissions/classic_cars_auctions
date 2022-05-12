import uuid
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from auctions.models import Bid, Car
from .models import Payment, PaymentLineItem
from .forms import PaymentForm

import stripe
import json


# @require_POST
# def cache_payment_data(request):
#     """Cach Payment"""
#     try:
#         pid = request.POST.get('client_secret').split('_secret')[0]
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         stripe.PaymentIntent.modify(pid, metadata={
#             'payment_info': json.dumps(request.session.get('payment_info', {})),
#             'save_info': request.POST.get('save_info'),
#             'username': request.user,
#         })
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, 'Sorry, your payment cannot be \
#             processed right now. Please try again later.')
#         return HttpResponse(content=e, status=400)


# @login_required()
def get_payment(request):
    """View to render Payment"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    unique_number = uuid.uuid4()

    payment_info = request.session.get('payment_info', {})
    for item in payment_info:
        car_id = item['car_id']
        winner_bid_id = item['winner_bid_id']
        car_price = item['car_price']
    payment_amount = car_price / 10
    winner_bid = Bid.objects.get(id=winner_bid_id)
    car = Car.objects.get(id=car_id)
    print(car_id)

    if request.method == 'POST':
        payment_data = {
            'payment_number': unique_number,
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'deposit': payment_amount,
        }
        payment_form = PaymentForm(payment_data)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.car_id = car_id
            payment.payment_number = unique_number
            payment.save()
            payment_line_item = PaymentLineItem(
                payment=payment,
                car=car,
                winner_bid=winner_bid,
                car_price=car_price,
                )
            payment_line_item.save()
            request.session['save_info'] = 'save_info' in request.POST
            return redirect(reverse('payment_success', args=[payment.payment_number]))
      
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        payment_info = request.session.get('payment_info', {})
        if not payment_info:
            messages.error(request, "Unauthorized access")
            return redirect(reverse('all_auctions'))

        stripe_total = round(payment_amount * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

        payment_form = PaymentForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    context = {
        'payment_form': payment_form,
        'car_price': car_price,
        'payment_amount': payment_amount,
        'car': car,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'payment/payment.html', context)


def payment_success(request, payment_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    payment = get_object_or_404(Payment, payment_number=payment_number)
    payment_line = get_object_or_404(PaymentLineItem, payment_id=payment.id)

    left_to_pay = payment_line.car_price - payment_line.car_price / 10

    messages.success(request, f'Order successfully processed! \
        Your order number is { payment_number }. A confirmation \
        email will be sent to { payment.email }.')

    if 'payment_info' in request.session:
        del request.session['payment_info']

    template = 'payment/payment_success.html'
    context = {
        'payment': payment,
        'left_to_pay': left_to_pay
    }

    return render(request, template, context)
