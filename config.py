import os
import re

from dotenv import load_dotenv

load_dotenv()
RESUME_LINK = os.getenv('RESUME_FIRST')
LOGIN_LINK = 'https://hh.ru/account/login?backurl=%2F&hhtmFrom=main'
WAIT_IN_SEC = 10
SEC_IN_HOUR = 3600
WAITING_TIME_SECONDS = 0
LOGIN = os.getenv('HH_LOGIN')
PASSWORD = os.getenv('HH_PASSWORD')
USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'


def get_wait_time_seconds(message):
    match = re.search(r'через (\d+) час', message)
    if match:
        wait_hours = int(match.group(1))
        return wait_hours * SEC_IN_HOUR
    return 0
