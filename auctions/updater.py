from apscheduler.schedulers.background import BackgroundScheduler
from .views import get_winner_bid, check_payments


def start():
    """function to run scheduler"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_payments, 'interval', minutes=60)
    scheduler.add_job(get_winner_bid, 'interval', minutes=60)
    scheduler.start()
