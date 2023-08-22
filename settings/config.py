import os

from dotenv import load_dotenv

load_dotenv()

RESUME_LINKS = [os.getenv('RESUME_FIRST')]
LOGIN = os.getenv('HH_LOGIN')
PASSWORD = os.getenv('HH_PASSWORD')
USER_AGENT = os.getenv('USER_AGENT')
LOGIN_LINK = 'https://hh.ru/account/login?backurl=%2F&hhtmFrom=main'

WAIT_TEN_SEC = 10
SLEEP_TIME = 2
SEC_IN_HOUR = 3600
WAITING_TIME_SECONDS = 0

CSS_SUBMIT_BUTTON = '[data-qa="expand-login-by-password"]'
CSS_PASSWORD_INPUT = '[data-qa="login-input-password"]'
CSS_ENTER_BUTTON = '[data-qa="account-login-submit"]'
CLASS_CAPTCHA = 'bloko-link__content'
NAME_LOGIN = 'login'
CSS_RESUME_UPDATE_BUTTON = '[data-qa="resume-update-button"]'
XPATH_COOKIE_BUTTON = (
    '//*[@id="HH-React-Root"]/div/div[1]/div/div/div/div[2]/button'
)
