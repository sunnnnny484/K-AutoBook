# --- coding: utf-8 ---
"""
A module for line-manga runner.
"""

import time
from config import SubConfigWithCookie
from runner import AbstractRunner
from linemanga.manager import Manager


class Runner(AbstractRunner):
    """
    A class for line-manga runner.
    https://manga.line.me/book/viewer?id=92dc0b4e-c5d4-4518-9fba-d78fb1e6b0f0
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, SubConfigWithCookie)

    def run(self):
        """
        Proceeds line-manga runner.
        """
        if self._set_cookie():
            self.driver.get('https://manga.line.me/store/')
            time.sleep(1)
        print('Loading page of inputted url (%s)' % self.url)
        self.driver.get(self.url)

        print('Open main page')

        destination = self.get_output_dir()
        print(f'Output Path : {destination}')

        manager = Manager(self.driver, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)
        return
