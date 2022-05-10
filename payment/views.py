import uuid
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings


import stripe
from auctions.models import Bid, Car
from .models import Payment, PaymentLineItem
from .forms import PaymentForm


@login_required()
def payment(request):
    """View to render Payment"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    unique_number = uuid.uuid4()
    payment_form = PaymentForm()

    payment_info = request.session.get('payment_info', {})

    if not payment_info:
        messages.error(request, "Unauthorized access")
        return redirect(reverse('all_auctions'))

    for item in payment_info:
        car_id = item['car_id']
        winner_bid_id = item['winner_bid_id']
        car_price = item['car_price']
        print(item)
    payment_amount = car_price / 10
    winner_bid = Bid.objects.get(id=winner_bid_id)
    car = Car.objects.get(id=car_id)

    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        country = request.POST['country']
        postcode = request.POST['postcode']
        town_or_city = request.POST['town_or_city']
        street_address1 = request.POST['street_address1']
        street_address2 = request.POST['street_address2']
        county = request.POST['county']

        new_payment = Payment(
                              payment_number=unique_number,
                              full_name=full_name,
                              email=email,
                              phone_number=phone_number,
                              country=country, postcode=postcode,
                              town_or_city=town_or_city,
                              street_address1=street_address1,
                              street_address2=street_address2, county=county,
                              deposit=payment_amount
                              )
        new_payment.save()
        try:
            Payment.objects.get(payment_number=unique_number)
        except Payment.DoesNotExist:
            messages.error(request, 'message1')
            new_payment.delete()
            return redirect('payment')
        payment_line_item = PaymentLineItem(
                    payment=new_payment,
                    car=car,
                    winner_bid=winner_bid,
                    car_price=car_price,
                    )
        payment_line_item.save()
        messages.success(request, 'success')
        return redirect('all_auctions')

        try:
            PaymentLineItem.objects.get(payment__payment_number=unique_number)
        except PaymentLineItem.DoesNotExist:
            messages.error(request,'message2')
            new_payment.delete()

    stripe_total = round(payment_amount * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

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
