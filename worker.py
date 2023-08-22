import logging
import time
from typing import Any, Optional, Tuple, cast

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from tenacity import retry, stop_after_attempt, wait_fixed

from settings.config import (CLASS_CAPTCHA, CSS_ENTER_BUTTON,
                             CSS_PASSWORD_INPUT, CSS_RESUME_UPDATE_BUTTON,
                             CSS_SUBMIT_BUTTON, LOGIN_LINK, NAME_LOGIN,
                             RESUME_LINKS, SLEEP_TIME, USER_AGENT,
                             WAIT_TEN_SEC, XPATH_COOKIE_BUTTON)
from settings.strings import (MSG_ALREADY_CLICKED, MSG_CAPTCHA, MSG_CLICKED,
                              MSG_LOGIN_START, MSG_LOGIN_SUCCESS,
                              MSG_NOT_FOUND, MSG_RESUME_NAME, MSG_RESUME_VALUE)

logger = logging.getLogger(__name__)


class BaseBrowser:
    def __init__(self, driver: Any):
        self.driver: WebDriver = driver
        self.actions: ActionChains = ActionChains(self.driver)
        self.wait: WebDriverWait = WebDriverWait(driver, WAIT_TEN_SEC)

    def click(self, locator: Tuple[str, str]) -> None:
        try:
            self.driver.find_element(*locator).click()
        except Exception as error_message:
            logger.error(error_message)

    def send_keys(self, locator: Tuple[str, str], keys: str) -> None:
        try:
            self.driver.find_element(*locator).send_keys(keys)
        except Exception as error_message:
            logger.error(error_message)

    def detect_element(self, element: Tuple[str, str]) -> Optional[WebElement]:
        try:
            return cast(WebElement, self.driver.find_element(*element))
        except selenium.common.exceptions.NoSuchElementException:
            logger.info(MSG_NOT_FOUND.format(element))
            return None


class LoginPage(BaseBrowser):
    def __init__(self, driver: Any):
        super().__init__(driver)
        self.login_input = (By.NAME, NAME_LOGIN)
        self.submit_button = (
            By.CSS_SELECTOR,
            CSS_SUBMIT_BUTTON,
        )
        self.password_input = (
            By.CSS_SELECTOR,
            CSS_PASSWORD_INPUT,
        )
        self.enter_button = (
            By.CSS_SELECTOR,
            CSS_ENTER_BUTTON,
        )
        self.captcha = (By.CLASS_NAME, CLASS_CAPTCHA)

    def login(self, username: str, password: str) -> None:
        self.send_keys(self.login_input, username)
        time.sleep(SLEEP_TIME)
        self.click(self.submit_button)
        time.sleep(SLEEP_TIME)
        self.send_keys(self.password_input, password)
        time.sleep(SLEEP_TIME)
        self.click(self.enter_button)
        time.sleep(SLEEP_TIME)
        if self.detect_element(self.captcha) is not None:
            raise ValueError(MSG_CAPTCHA)


class ResumePage(BaseBrowser):
    def __init__(self, driver: Any):
        super().__init__(driver)
        self.resume_update_button = (
            By.CSS_SELECTOR,
            CSS_RESUME_UPDATE_BUTTON,
        )
        self.cookie_button = (
            By.XPATH,
            XPATH_COOKIE_BUTTON,
        )

    @retry(wait=wait_fixed(SLEEP_TIME), stop=stop_after_attempt(5))
    def update_resume(self) -> None:
        if self.detect_element(self.cookie_button) is not None:
            self.click(self.cookie_button)
        button = self.detect_element(self.resume_update_button)
        if button and button.is_enabled():  # type: ignore
            self.click(self.resume_update_button)
            logger.info(MSG_CLICKED)
            time.sleep(SLEEP_TIME)
        else:
            logger.info(MSG_ALREADY_CLICKED)


class TestHH:
    chrome_options: Options

    def __init__(self) -> None:
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
        chrome_options.add_experimental_option(
            'useAutomationExtension', False)
        chrome_options.add_argument(f'user-agent={USER_AGENT}')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(WAIT_TEN_SEC)
        self.driver.get(LOGIN_LINK)

    def run(self, username: str, password: str) -> None:
        logger.info(MSG_RESUME_VALUE.format(len(RESUME_LINKS)))
        login_page = LoginPage(self.driver)
        logger.info(MSG_LOGIN_START)
        login_page.login(username, password)
        logger.info(MSG_LOGIN_SUCCESS)
        time.sleep(3)
        for link in RESUME_LINKS:
            logger.info(MSG_RESUME_NAME.format(link))
            self.driver.get(link)
            resume_page = ResumePage(self.driver)
            resume_page.update_resume()
        self.driver.quit()
