from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from payment.models import Payment
from auctions.models import Bid

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """ Display the user's profile. """
    user_id = request.user.id
    profile = get_object_or_404(UserProfile, user=request.user)
    user_bids = Bid.objects.filter(user_id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    payments = profile.payment.all()

    template = 'profiles/profile.html'
    context = {
        'payments': payments,
        'form': form,
        'user_bids':  user_bids,
        'on_profile_page': True,
    }
    return render(request, template, context)


@login_required
def payment_history(request, payment_number):
    """views  to render payment history"""
    payment = get_object_or_404(Payment, payment_number=payment_number)

    messages.info(request, (
        f'This is a past confirmation for a payment number {payment_number}. '
        'A confirmation email was sent on the Payment date.'
    ))

    template = 'payment/payment_success.html'
    context = {
        'payment': payment,
        'from_profile': True,
    }

    return render(request, template, context)
