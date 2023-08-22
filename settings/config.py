import os
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()

RESUME_LINKS: List[Optional[str]] = [os.getenv('RESUME_FIRST')]
LOGIN: Optional[str] = os.getenv('HH_LOGIN')
PASSWORD: Optional[str] = os.getenv('HH_PASSWORD')
USER_AGENT: Optional[str] = os.getenv('USER_AGENT')
LOGIN_LINK: str = 'https://hh.ru/account/login?backurl=%2F&hhtmFrom=main'

WAIT_TEN_SEC: int = 10
SLEEP_TIME: int = 2
SEC_IN_HOUR: int = 3600
WAITING_TIME_SECONDS: int = 0

CSS_SUBMIT_BUTTON: str = '[data-qa="expand-login-by-password"]'
CSS_PASSWORD_INPUT: str = '[data-qa="login-input-password"]'
CSS_ENTER_BUTTON: str = '[data-qa="account-login-submit"]'
CLASS_CAPTCHA: str = 'bloko-link__content'
NAME_LOGIN: str = 'login'
CSS_RESUME_UPDATE_BUTTON: str = '[data-qa="resume-update-button"]'
XPATH_COOKIE_BUTTON: str = '//*[@id="HH-React-Root"]/div/div[1]/div/div/div/div[2]/button'
