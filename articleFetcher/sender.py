from datetime import datetime
from articleFetcher import schedule_mail
from apscheduler.schedulers.blocking import BlockingScheduler


def start():
    scheduler = BlockingScheduler()
