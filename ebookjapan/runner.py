# --- coding: utf-8 ---
"""
A module for ebookjapan runner.
"""

import time

from selenium.webdriver.common.by import By

from runner import AbstractRunner
from ebookjapan.login import YahooLogin
from ebookjapan.manager import Manager
from ebookjapan.config import SubConfig


class Runner(AbstractRunner):
    """
    A class for ebookjapan runner.

    https://ebookjapan.yahoo.co.jp/books/145222/A000100547

    if you want to scrape purchased items, set your yahoo japan login settings to 'use password login'
    instead of other login methods like 'sms authentication'.
    """

    is_login = False
    """
    ログイン状態
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, SubConfig)

    def run(self):
        """
        Proceeds ebookjapan runner.
        """
        if self._set_cookie():
            time.sleep(1)
            self.driver.get('https://ebookjapan.yahoo.co.jp/')
            time.sleep(1)
        else:
            if self.sub_config.needs_login and not self._is_login() and not self._login():
                print('cannot login')
                return
        print('Loading page of inputted url (%s)' % self.url)
        self.driver.get(self.url)

        if self._move_main_page():
            print('Open main page')
        elif self._move_demo_page():
            print('Open demo page')
        else:
            print('Failed to retrieve page')
            return

        destination = self.get_output_dir()
        print(f'Output Path : {destination}')

        manager = Manager(self.driver, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)

    def _is_login(self):
        """
        ログイン状態の確認を行う
        @return ログインしている場合に True を、していない場合に False を返す
        """
        if Runner.is_login:
            return True
        self.driver.get(self.url)
        if len(self.driver.find_elements(By.CSS_SELECTOR, '.login')) == 0:
            Runner.is_login = True
            return True
        return False

    def _login(self):
        """
        ログイン処理を行う
        @return ログイン成功時に True を返す
        """
        if self.sub_config.username and self.sub_config.password:
            yahoo = YahooLogin(
                self.driver,
                self.sub_config.username,
                self.sub_config.password)
        else:
            yahoo = YahooLogin(self.driver)
        if yahoo.login():
            Runner.is_login = True
            return True
        return False

    def _move_main_page(self):
        """
        Goes to actual book page.
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.btn.btn--primary.btn--read')
        if len(elements) != 0 and '読む' in elements[0].text:
            elements[0].click()
            return True
        return False

    def _move_demo_page(self):
        """
        実際の本の試し読みページに移動する
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.book-main__purchase > a.btn')
        if len(elements) != 0 and '試し読み' in elements[0].text:
            elements[0].click()
            return True
        return False
