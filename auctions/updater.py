from apscheduler.schedulers.background import BackgroundScheduler
from .views import get_winner_bid, check_payments


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_payments, 'interval', seconds=35)
    scheduler.add_job(get_winner_bid, 'interval', seconds=35)
    scheduler.start()
    # scheduler.shutdown()