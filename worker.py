import logging
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tenacity import retry, stop_after_attempt, wait_fixed

from config import LOGIN_LINK, RESUME_LINK, USERAGENT, WAIT_IN_SEC

logger = logging.getLogger(__name__)


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_input = (By.NAME, 'login')
        self.submit_button = (
            By.CSS_SELECTOR,
            '[data-qa="expand-login-by-password"]',
        )
        self.password_input = (
            By.CSS_SELECTOR,
            '[data-qa="login-input-password"]',
        )
        self.enter_button = (
            By.CSS_SELECTOR,
            '[data-qa="account-login-submit"]',
        )
        self.captcha = (By.CLASS_NAME, 'bloko-link__content')

    def login(self, username, password):
        self.driver.find_element(*self.login_input).send_keys(username)
        time.sleep(2)
        self.driver.find_element(*self.submit_button).click()
        time.sleep(2)
        self.driver.find_element(*self.password_input).send_keys(password)
        time.sleep(2)
        self.driver.find_element(*self.enter_button).click()
        time.sleep(2)
        try:
            self.driver.find_element(*self.captcha)
            raise ValueError('Get captched!')
        except selenium.common.exceptions.NoSuchElementException:
            pass


class ResumePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, WAIT_IN_SEC)
        self.actions = ActionChains(self.driver)
        self.resume_update_button = (
            By.CSS_SELECTOR,
            '[data-qa="resume-update-button"]',
        )
        self.cookie_button = (
            By.XPATH,
            '//*[@id="HH-React-Root"]/div/div[1]/div/div/div/div[2]/button',
        )

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
    def update_resume(self):
        try:
            self.driver.find_element(*self.cookie_button).click()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        try:
            button = self.driver.find_element(*self.resume_update_button)
            if button.is_enabled():
                self.actions.move_to_element(button).click(button).perform()
                logger.info('Clicked!')
                time.sleep(3)
            else:
                logger.info('Resume is already clicked')
        except Exception as e:
            logger.info(e)


class TestHH:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled'
        )
        chrome_options.add_argument('--enable-webgl')
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
        chrome_options.add_experimental_option('useAutomationExtension', False)

        chrome_options.add_argument(f'user-agent={USERAGENT}')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(WAIT_IN_SEC)
        self.driver.get(LOGIN_LINK)

    def run(self, username, password):
        logger.info('Process started')
        login_page = LoginPage(self.driver)
        logger.info('Logging into HH account')
        login_page.login(username, password)
        logger.info('Logged in successfully!')
        time.sleep(3)

        self.driver.get(RESUME_LINK)
        resume_page = ResumePage(self.driver)
        resume_page.update_resume()
        self.driver.quit()
