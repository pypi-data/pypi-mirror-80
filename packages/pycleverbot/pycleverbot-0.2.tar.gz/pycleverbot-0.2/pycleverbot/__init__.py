from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from os.path import join, dirname
from tempfile import gettempdir
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class NoSession(RuntimeError):
    """ forgot to call new_session()"""


class Cleverbot:
    def __init__(self, exec_path=None, headless=True):
        self.options = Options()
        if headless:
            self.options.headless = True
        self.exec_path = exec_path
        self.driver = None
        self.utterances = []

    def new_session(self):
        self.utterances = []
        self.stop()
        if self.exec_path:
            self.driver = webdriver.Firefox(executable_path=self.exec_path,
                                            options=self.options)
        else:
            self.driver = webdriver.Firefox(options=self.options)
        self._accept()

    def _accept(self):
        self.driver.get("https://www.cleverbot.com/")
        accept_btn = self.wait_and_get_xpath(
                                  "/html/body/div[1]/div[2]/div[1]/div/div/form/input")
        accept_btn.click()

    def wait_and_get_xpath(self, xpath, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(
            (By.XPATH, xpath)))
        return element

    def get_xpath(self, xpath, timeout=10, wait=False):
        if wait:
            return self.wait_and_get_xpath(xpath, timeout)
        element = self.driver.find_element_by_xpath(xpath)
        return element

    def ask(self, utterance):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        xpath = "/html/body/div[1]/div[2]/div[3]/form/input[1]"
        input = self.wait_and_get_xpath(xpath)
        input.send_keys(utterance)
        input.submit()
        share_marker = '//*[@id="snipTextIcon"]'
        _ = self.wait_and_get_xpath(share_marker)
        answer = self.get_xpath('/html/body/div[1]/div[2]/div[3]/p[9]/span[1]').text
        self.utterances.append((utterance, answer))
        return answer

    def save_screenshot(self, path=None):
        path = path or join(gettempdir(), "pycleverbot.png")
        self.driver.save_screenshot(path)
        return path

    def stop(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def __enter__(self):
        self.new_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()