import datetime
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .email import send_confirmation_email

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from payment.models import Payment
from .models import Car, Bid
from .filters import CarFilter
from .forms import BidForm, CarForm


def all_auctions(request):
    """ A view to return all cars and for sorting cars """

    cars = Car.objects.all()

    auctions_filter = CarFilter(request.GET, queryset=cars)
    cars = auctions_filter.qs

    if not cars:
        cars = Car.objects.all()

        messages.error(request, "Sorry, but we couldn't find any cars matching"
                                " your criteria")

    context = {
        'cars': cars,
        'auctions_filter': auctions_filter,
    }

    return render(request, 'auctions/auctions.html', context)


def auction_detail(request, car_id):
    """ A view to return car and auctions detail """
    bid_subject_url = 'auctions/confirmation_emails/'\
                      'bid_confirmation_email_subject.txt'
    bid_body_url = 'auctions/confirmation_emails/'\
                   'bid_confirmation_email_body.txt'
    message = 'Congratulations Your bid is the winning bid!!!'\
              'You Won this auction.  Please proceed with the payment.'

    payment_info = []
    request.session['payment_info'] = payment_info
    highest_bid_obj = None

    user_bid = 0
    form = BidForm()
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

    car = get_object_or_404(Car, id=car_id)
    bids = Bid.objects.filter(car_id=car_id)

    current_date = timezone.now()
    start_time = car.timeStart
    end_time = car.timeEnd
    auction_is_on = current_date > start_time and current_date < end_time

    if bids:
        highest_bid_obj = Bid.objects.filter(
                              car_id=car_id
                              ).order_by('-amount')[0]

        min_bid = highest_bid_obj.amount + 50

    else:
        min_bid = car.reservedPrice - 300

    if request.method == 'POST':
        user_bid = request.POST['user_bid']
        if not user_bid:
            messages.error(request, 'Oops!! Something went wrong.'
                           ' Please enter your bid again.')

        else:
            bid = user_bid

            if int(bid) >= min_bid:
                new_bid = Bid(car=car, user=user,  amount=bid,
                              time=current_date, winnerBid=False)
                new_bid.save()
                send_confirmation_email(new_bid, bid_subject_url, bid_body_url)
                messages.success(request, f'Your bid for {bid} € was'
                                 ' successfully added')
                # car_obj_bids = Bid.objects.filter(car_id=car_id)
                # for bid in car_obj_bids:
                #     print(bid.user)
                return redirect('auction_detail', car_id=car_id)
            else:
                messages.error(request, f'Your bid should be equal'
                               f' or superior to {min_bid} €')

    existing_payment = Payment.objects.filter(car_id=car_id)
    if existing_payment:
        payment_info = None
    else:
        if bids:
            if (highest_bid_obj.winnerBid and
               highest_bid_obj.user.id == user_id):

                messages.success(request, message)
                payment_info. append({
                    'car_id': car_id,
                    'winner_bid_id': highest_bid_obj.id,
                    'car_price': highest_bid_obj.amount,
                })
                request.session['payment_info'] = payment_info

    context = {
        'car': car,
        'auction_is_on': auction_is_on,
        'bids': bids,
        'highest_bid_obj': highest_bid_obj,
        'form': form,
        'min_bid': min_bid,
        'existing_payment': existing_payment,
        'on_auction_detail_page': True,
    }

    return render(request, 'auctions/auction_detail.html', context)


@login_required
def add_auction(request):
    """ Add an auction to the website """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, 'Successfully added new auction!')
            return redirect(reverse('auction_detail', args=[car.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure \
                           the form is valid.')
    else:
        form = CarForm()

    template = 'auctions/add_auction.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_auction(request, car_id):
    """ Edit an auction """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('auction_detail', args=[car.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure \
                                    the form is valid.')
    else:
        form = CarForm(instance=car)
        messages.info(request, f'You are editing {car.make}, {car.model}')

    template = 'auctions/edit_auction.html'

    context = {
        'form': form,
        'car': car,
    }

    return render(request, template, context)


@login_required
def delete_auction(request, car_id):
    """ Delete an auction from the website """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, 'Auction deleted!')
    return redirect(reverse('all_auctions'))


@login_required
def admin(request):
    """ render Admin view """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    cars = Car.objects.all()

    template = 'auctions/admin.html'

    context = {
        'cars': cars,
    }
    return render(request, template, context)


def get_winner_bid():
    """
        function to specify the winner's bid and to extend
        auctions  if the winning bid does not exist.
    """
    winner_subject_url = 'auctions/confirmation_emails/'\
                         'winner_confirmation_email_subject.txt'
    winner_body_url = 'auctions/confirmation_emails/'\
                      'winner_confirmation_email_body.txt'
    current_date = timezone.now()
    cars = Car.objects.all()

    for car in cars:
        new_auction_end = current_date + timedelta(hours=48)
        bids = Bid.objects.filter(car_id=car.id)

        if current_date >= car.timeEnd:
            if bids:
                highest_bid = Bid.objects.filter(
                                 car_id=car.id).order_by('-amount')[0]
                if not highest_bid.winnerBid:
                    if highest_bid.amount >= car.reservedPrice:
                        Bid.objects.filter(
                           id=highest_bid.id).update(winnerBid=True)
                        send_confirmation_email(highest_bid, winner_subject_url, winner_body_url)
                    else:
                        Car.objects.filter(
                            id=car.id).update(timeEnd=new_auction_end)
            else:
                Car.objects.filter(id=car.id).update(timeEnd=new_auction_end)


def check_payments():
    """
    function to check for payments
    if payment exists if not
    the winner bid is cancled and
    it goes to second highest bidder
    """
    defaulter_subject_url = 'auctions/confirmation_emails/'\
                            'payment_defaulter_email_subject.txt',
    defaulter_body_url = 'auctions/confirmation_emails/'\
                         'payment_defaulter_email_body.txt'
    current_date = timezone.now()
    bids = Bid.objects.all()

    for bid in bids:
        if bid.winnerBid:
            payment_deadline = bid.car.timeEnd + timedelta(hours=48)
            payment = Payment.objects.filter(bids_id=bid.id)
            if not payment:
                if current_date > payment_deadline:
                    send_confirmation_email(bid, defaulter_subject_url, defaulter_body_url)
                    Bid.objects.filter(id=bid.id).delete()
