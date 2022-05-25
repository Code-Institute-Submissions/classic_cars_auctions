from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from auctions.models import Car, Bid
from .models import Payment

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, payment):
        """Send the user a confirmation email"""
        cust_email = payment.email
        subject = render_to_string(
            'payment/confirmation_emails/confirmation_email_subject.txt',
            {'payment': payment})
        body = render_to_string(
            'payment/confirmation_emails/confirmation_email_body.txt',
            {'payment': payment, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """

        intent = event.data.object
        save_info = intent.metadata.save_info
        payment_info = intent.metadata.payment_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        deposit = round(intent.charges.data[0].amount / 100, 2)

        for item in json.loads(payment_info):
            car_id = item['car_id']
            winner_bid_id = item['winner_bid_id']

        winner_bid = Bid.objects.get(id=winner_bid_id)
        car = Car.objects.get(id=car_id)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        payment_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                payment = Payment.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    deposit=deposit,
                    car=car,
                    bids=winner_bid,
                )
                payment_exists = True
                break
            except Payment.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if payment_exists:
            self._send_confirmation_email(payment)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} |' +
                'SUCCESS: Verified Payment already in database',
                status=200)
        else:
            payment = None
            payment = Payment.objects.create(
                full_name=shipping_details.name,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                country=shipping_details.address.country,
                postcode=shipping_details.address.postal_code,
                town_or_city=shipping_details.address.city,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                county=shipping_details.address.state,
                deposit=deposit,
                car=car,
                bids=winner_bid,
            )
        self._send_confirmation_email(payment)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created Payment in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
