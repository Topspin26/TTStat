from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import random


class Driver:
    def __init__(self, driver_name, options=None):
        options = options or []
        self.driver_name = driver_name
        self.options = list(options)
        self.driver = None

    def start(self):
        if self.driver_name == 'chrome':
            chrome_options = ChromeOptions()
            for e in self.options:
                chrome_options.add_argument(e)
            self.driver = webdriver.Chrome('chromedriver_win32/chromedriver',
                                           chrome_options=chrome_options)
        elif self.driver_name == 'firefox':
            firefox_options = FirefoxOptions()
            for e in self.options:
                firefox_options.add_argument(e)
            self.driver = webdriver.Firefox(executable_path='geckodriver-v0.20.1-win64/geckodriver',
                                            options=firefox_options)

    def run(self, url, sleep_time=0, is_random=1):
        if self.driver is None:
            self.start()
        self.driver.refresh()
        self.driver.get(url)
        time.sleep(sleep_time + is_random * random.random())

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as exc:
                print(exc)
                pass

