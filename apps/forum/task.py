from __future__ import absolute_import, unicode_literals
import time

from celery import shared_task

@shared_task(name="messages")
def messages():
    print('a')
    time.sleep(5)
    print("OK")
