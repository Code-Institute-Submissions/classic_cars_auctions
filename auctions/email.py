from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_confirmation_email(obj, subject_url, body_url):
    """Send the user a confirmation email"""
    cust_email = obj.user.email
    subject = render_to_string(
        subject_url,
        {'obj': obj})
    body = render_to_string(
        body_url,
        {'obj': obj, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )


def send_outbid_email(obj, new_amount, subject_url, body_url):
    """Send the user a confirmation email"""
    cust_email = obj.user.email
    subject = render_to_string(
        subject_url,
        {'obj': obj, 'new_amount': new_amount})
    body = render_to_string(
        body_url,
        {'obj': obj, 'new_amount': new_amount,
         'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
