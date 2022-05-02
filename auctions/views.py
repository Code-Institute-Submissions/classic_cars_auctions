from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Car, Bid
from .filters import CarFilter
from .forms import BidForm


def all_auctions(request):
    """ A view to return all cars and for sorting cars """

    cars = Car.objects.all()

    if request.method == 'POST':
        user_bid = request.POST['bid']
        print(user_bid)

    auctions_filter = CarFilter(request.GET, queryset=cars)
    cars = auctions_filter.qs

    context = {
        'cars': cars,
        'auctions_filter': auctions_filter,
    }

    return render(request, 'auctions/auctions.html', context)


def auction_detail(request, car_id):
    """ A view to return car and auctions detail """
    # highest_bid = None
    form = None
    car = get_object_or_404(Car, id=car_id)

    current_date = timezone.now()
    start_time = car.timeStart
    end_time = car.timeEnd
    auction_is_on = current_date > start_time and current_date < end_time
    # auction_not_ended = current_date < auction_ended

    bids = Bid.objects.filter(car_id=car_id)

    if bids:
        highest_bid = Bid.objects.filter(car_id=car_id).order_by('-amount')[0].amount
        min_bid = highest_bid + 50
    else:
        min_bid = car.reservedPrice - 300

    request.session['car_id'] = car_id
    request.session['min_bid'] = min_bid

    # if current_date >= end_time:
    #     winner_bid(car_id)

    context = {
        'car': car,
        'auction_is_on': auction_is_on,
        # 'auction_not_ended': auction_not_ended,
        'bids': bids,
        'min_bid':  min_bid,
        'form': form,
    }

    return render(request, 'auctions/auction_detail.html', context)


def get_user_bid(request):
    """ A view to return car and auctions detail """
    user_bid = 0
    if request.user.is_authenticated:
        user_id = request.user.id
    car_id = request.session['car_id']
    car = get_object_or_404(Car, id=car_id)
    bids = Bid.objects.filter(car_id=car_id)

    if bids:
        highest_bid = Bid.objects.filter(car_id=car_id).order_by('-amount')[0].amount
        min_bid = highest_bid + 50
    else:
        min_bid = car.reservedPrice - 100

    current_date = timezone.now()

    form = BidForm()
    if request.method == 'POST':
        user_bid = request.POST['user_bid']

    if user_bid:
        bid = int(user_bid)
        if bid >= int(min_bid):
            new_bid = Bid(car=car, user_id=user_id,  amount=bid,
                          time=current_date, winnerBid=False)
            new_bid.save()
            messages.success(request, f'Your bid {bid} € was successfully'
                             ' added')
            return redirect('get_user_bid')
        else:
            messages.error(request, f'Your bid should be equal to {min_bid}'
                                    ' or superior')

    context = {
        'form': form,
        'min_bid': min_bid,
    }
    return render(request, 'auctions/user_bid.html', context)


def winner_bid():
    """function to specify winner bid"""
    print('yyyy')
    # car_id = request.session['car_id']
    # current_date = timezone.now()
    # car = get_object_or_404(Car, id=car_id)
    # bids = Bid.objects.filter(car_id=car_id)
    # new_auction_end = car.timeEnd + timedelta(hours=48)
    # if current_date >= car.timeEnd:
    #     if bids:
    #         highest_bid = Bid.objects.filter(car_id=car_id).order_by('-amount')[0]
    #         highest_bid_amount = highest_bid.amount
    #         highest_bid_id = highest_bid.id

    #         if highest_bid_amount > car.reservedPrice:
    #             Bid.objects.filter(id=highest_bid_id).update(winnerBid=True)
    #         else:
    #             Car.objects.filter(id=car_id).update(timeEnd=new_auction_end)
    #     else:
    #         Car.objects.filter(id=car_id).update(timeEnd=new_auction_end)
