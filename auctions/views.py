from django.shortcuts import render, get_object_or_404
# from django.contrib import messages
from django.utils import timezone
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
        min_bid = car.reservedPrice - 100

    request.session['car_id'] = car_id
    request.session['min_bid'] = min_bid

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
    min_bid = request.session['min_bid']
    car_id = request.session['car_id']

    car = get_object_or_404(Car, id=car_id)

    current_date = timezone.now()

    form = BidForm()
    if request.method == 'POST':
        user_bid = int(request.POST['user_bid'])

    if user_bid >= int(min_bid):
        new_bid = Bid(car=car, user_id=user_id,  amount=user_bid,
                      time=current_date, winnerBid=False)
        new_bid.save()
    else:
        print("Your bid should be equal or superior to {% min_bid %}")

    context = {
        'form': form,
        'min_bid': min_bid,
    }
    return render(request, 'auctions/user_bid.html', context)


# def winner_bid(car_id):
#     """function to specify winner bid"""
#     car = get_object_or_404(Car, id=car_id)
#     bids = list(Bid.objects.filter(car_id=car_id))
#     if len(bids) != 0:
#         win_bid = highest_bid(bids)
#     if win_bid > car.reservedPrice:
#         new_bid = Bid(car=car, user_id=user_id,  amount=win_bid,
#                       time=current_date,
#                          winnerBid=False)
#         new_bid.save()

# def bid(request, auction_id):
#     """ A view to bid """
    # user_bid = None
    # if request.method == 'POST':
    #     bid = Bid(car=)
    #     user_bid = int(request.POST.get('bid'))
    # print(auction_id)
    # return render(request, 'auctions/bid.html')
