# coding=utf-8
from datetime import datetime
import time
import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig()

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


def run_command(cmd):
    print('The time is: %s' % datetime.now())
    os.system(cmd)


def start(cmd):
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_command, args=(cmd,), trigger='cron', day_of_week='0-6', hour='20', minute='30', second='00')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            time.sleep(20)
            print('sleep! %s' % datetime.now())
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')

if __name__ == '__main__':
    start(sys.argv[1])
