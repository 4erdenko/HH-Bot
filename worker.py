import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, wait_fixed, stop_after_attempt

from config import WAIT_IN_SEC, RESUME_LINK, LOGIN_LINK

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
        self.driver.find_element(*self.submit_button).click()
        self.driver.find_element(*self.password_input).send_keys(password)
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
        self.actions = ActionChains(self.driver)
        self.resume_update_button = (
            By.CSS_SELECTOR,
            '[data-qa="resume-update-button_actions"]',
        )
        self.resume_update_button_tooltip = (
            By.CSS_SELECTOR,
            '[data-qa="resume-update-button-tooltip"]',
        )

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
    def update_resume(self):
        try:
            resume_update_element = WebDriverWait(
                self.driver, WAIT_IN_SEC
            ).until(EC.element_to_be_clickable(self.resume_update_button))
        except selenium.common.exceptions.NoSuchElementException:
            return logger.error('Element not found')
        if resume_update_element.text == 'Поднимать автоматически':
            self.actions.move_to_element(resume_update_element).perform()
            tooltip = WebDriverWait(self.driver, WAIT_IN_SEC).until(
                EC.visibility_of_element_located(
                    self.resume_update_button_tooltip
                )
            )
            tooltip_message = tooltip.text
            logger.info(tooltip_message)

        else:
            try:
                resume_update_element.click()
            except Exception as error:
                logger.error(error)
            logger.info('Successfully UP resume!')


class TestHH:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')
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
