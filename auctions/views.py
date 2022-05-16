from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from payment.models import Payment
from .models import Car, Bid
from .filters import CarFilter
from .forms import BidForm, CarForm



def all_auctions(request):
    """ A view to return all cars and for sorting cars """

    cars = Car.objects.all()

    if request.method == 'POST':
        user_bid = request.POST['bid']

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
    payment_info = []
    request.session['payment_info'] = payment_info
    highest_bid_obj = None
    
    # winner_bid = None
    user_bid = 0
    form = BidForm()
    if request.user.is_authenticated:
        user_id = request.user.id

    car = get_object_or_404(Car, id=car_id)
    bids = Bid.objects.filter(car_id=car_id)

    current_date = timezone.now()
    start_time = car.timeStart
    end_time = car.timeEnd
    auction_is_on = current_date > start_time and current_date < end_time

    if bids:
        highest_bid_obj = Bid.objects.filter(car_id=car_id).order_by('-amount')[0]
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
                new_bid = Bid(car=car, user_id=user_id,  amount=bid,
                              time=current_date, winnerBid=False)
                new_bid.save()
                messages.success(request, f'Your bid for {bid} € was'
                                 ' successfully added')
                return redirect('auction_detail', car_id=car_id)
            else:
                messages.error(request, f'Your bid should be equal'
                               f' or superior to {min_bid} €')

    existing_payment = Payment.objects.filter(car_id=car_id)
    if existing_payment:
        payment_info = None
    else:
        if bids:
            if highest_bid_obj.winnerBid and highest_bid_obj.user.id == user_id:
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
    }

    return render(request, 'auctions/auction_detail.html', context)


def add_auction(request):
    """ Add a product to the store """
    form = CarForm()
    template = 'auctions/add_auction.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def get_winner_bid(car_id):
    """function to specify winner bid"""
    current_date = timezone.now()
    car = get_object_or_404(Car, id=car_id)
    bids = Bid.objects.filter(car_id=car_id)
    new_auction_end = car.timeEnd + timedelta(hours=48)
    if current_date >= car.timeEnd:
        if bids:
            highest_bid = Bid.objects.filter(car_id=car_id).order_by('-amount')[0]
            highest_bid_amount = highest_bid.amount
            highest_bid_id = highest_bid.id

            if highest_bid_amount > car.reservedPrice:
                Bid.objects.filter(id=highest_bid_id).update(winnerBid=True)
            else:
                Car.objects.filter(id=car_id).update(timeEnd=new_auction_end)
        else:
            Car.objects.filter(id=car_id).update(timeEnd=new_auction_end)
