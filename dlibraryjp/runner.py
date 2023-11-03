# --- coding: utf-8 ---
"""
d-library.jp module
"""

import re
import time

from selenium.webdriver.common.by import By

from config import SubConfigWithCookie
from runner import AbstractRunner
from dlibraryjp.manager import Manager


class Runner(AbstractRunner):
    """
    d-library.jp scraper
    https://www.d-library.jp/meguro/g0102/libcontentsinfo/?conid=163577&m=%E7%B5%82%E7%82%B9%E3%81%AE%E3%81%82%E3%81%AE%E5%AD%90+%EF%BC%88%E6%96%87%E6%98%A5%E3%82%A6%E3%82%A7%E3%83%96%E6%96%87%E5%BA%AB%EF%BC%89
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, SubConfigWithCookie)

    def run(self):
        """
        run d-library.jp
        """
        if self._set_cookie():
            print("cookie has set")
            self.driver.get(self.sub_config.top_url)
            time.sleep(1)
        print('Loading page of inputted url (%s)' % self.url)
        self.driver.get(self.url)

        if self._move_main_page():
            print('Open main page')
        else:
            print('Failed to retrieve page')
            return

        destination = self.get_output_dir()
        print(f'Output Path : {destination}')

        manager = Manager(self.driver, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)

    def _move_main_page(self):
        """
        Goes to actual book page.
        TODO works on headless mode only why???
        """
        print(self.driver.current_url)
        try:
            print("search read button")
            button = self.driver.find_element(By.CSS_SELECTOR, 'div.rental_buttonside > button')
            time.sleep(2)
        except Exception:
            print("search login button")
            button = self.driver.find_element(By.CSS_SELECTOR, '#loginForm > button')
            button.click()
            time.sleep(2)

            self.driver.get(self.url)
            print(self.driver.current_url)
            return self._move_main_page()

        script = button.get_attribute('onclick')
        if script is None:
            button = self.driver.find_element(By.CSS_SELECTOR, '#loginInput button')
            button.click()
            time.sleep(2)

            return self._move_main_page()

        url = re.sub(r"^.*?'", "", script)
        url = re.sub(r"'.*$", "", url)
        # print(f"[{url}]")
        self.driver.get(url)
        return True
