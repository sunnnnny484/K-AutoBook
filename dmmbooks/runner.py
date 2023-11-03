# --- coding: utf-8 ---
"""
A module for dmm books runner.
"""

import time

from selenium.webdriver.common.by import By

from config import SubConfigWithCookie
from runner import AbstractRunner
from dmmbooks.manager import Manager


class Runner(AbstractRunner):
    """
    A class for dmm books runner.
    https://book.dmm.com/library/?item_id=b900qkds03987
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, SubConfigWithCookie)

    def run(self):
        """
        Proceeds line-manga runner.
        """
        if self._set_cookie():
            self.driver.get('https://book.dmm.com/')
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

        manager = Manager(
            self.driver, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)
        return

    def _move_main_page(self):
        """
        Goes to actual book page.
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.m-boxListBookProductBlock__btn > div')
        if len(elements) != 0 and '読む' in elements[0].text:
            elements[0].click()
            return True
        return False
