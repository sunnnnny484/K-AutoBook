# --- coding: utf-8 ---
"""
ebookjapanを使用するためにYahooアカウントでログインするためのクラスモジュール
"""

from getpass import getpass
from urllib import request
from PIL import Image
import io
import time
from selenium.webdriver.remote.webdriver import WebDriver


class YahooLogin(object):
    """
    Yahooアカウントでログインするためのクラス
    """

    LOGIN_URL = 'https://login.yahoo.co.jp/config/login'
    """
    ログインページの URL
    """

    YAHOO_JAPAN_URL = 'https://www.yahoo.co.jp/'
    """
    Yahoo! JAPAN の URL
    """

    ONE_TIME_PASSWORD_URL = 'https://protect.login.yahoo.co.jp/otp/auth'
    """
    ログイン時にワンタイムパスワードを求めるページの URL
    """

    def __init__(self, driver, yahoo_id=None, password=None):
        """
        Yahoo でログインするためのコンストラクタ
        @param driver selenium のブラウザインスタンス
        @param yahoo_id ヤフー ID
        @param password パスワード
        """
        self.driver: WebDriver = driver
        """
        splinter のブラウザインスタンス
        """
        self.yahoo_id = yahoo_id
        """
        Yahoo ID
        None が設定されている場合はユーザ入力を求める
        """
        self.password = password
        """
        パスワード
        None が設定されている場合はユーザ入力を求める
        """
        return

    def login(self):
        """
        ログインを行う
        @return ログイン成功時に True を返す
        """
        print('Loading Yahoo JAPAN! top page')
        self.driver.get(self.YAHOO_JAPAN_URL)
        print('Loading login page')
        url = self.driver.find_elements_by_css_selector('#Login [data-rapid_p]')[0]['href']
        self.driver.get(url)
        for try_count in range(4):
            yahoo_id = input('Input Yahoo ID > ') if (
                self.yahoo_id is None) else self.yahoo_id
            password = getpass('Input Password > ') if (
                self.password is None) else self.password
            print('Trying login: ' + yahoo_id)
            self.driver.find_element_by_id('login').send_keys(yahoo_id)
            print('Confirm Yahoo JAPAN! ID')
            self.driver.find_element_by_id('btnNext').click()
            time.sleep(1)
            self.driver.execute_script(
                'element = document.getElementById("passwd");' +
                'element.disabled = false;' +
                'element.readOnly = false;')
            self.driver.find_element_by_id('passwd').send_keys(password)
            self.driver.find_element_by_id('btnSubmit').click()
            print('Trying login')
            if self._is_login_error():
                print('ログインに失敗しました')
                if self.yahoo_id is not None and self.password is not None:
                    return False
                continue
            for count in range(3):
                if self._is_image_captcha():
                    if not self._show_image_captcha():
                        return False
                    _result = input('Input Captcha > ')
                    self.driver.find_element_by_id('captchaAnswer').send_keys(_result)
                    self.driver.find_elements_by_css_selector('input[type=image]')[0].click()
                elif self._is_login_page():
                    break
                else:
                    break
                if count == 2 and self._is_image_captcha():
                    print('画像キャプチャが一致しませんでした')
                    return False
            if not self._is_login_page():
                one_time_password = None
                is_succeeded_login = False
                for count in range(4):
                    if self._is_required_one_time_password():
                        if one_time_password is not None:
                            print('Invalid one time password')
                        one_time_password = input(
                            'Input one time password > ')
                        self.driver.find_element_by_id('verify_code').send_keys(one_time_password)
                        self.driver.find_elements_by_css_selector('[type=submit]')[0].click()
                    else:
                        is_succeeded_login = True
                        break
                print('Succeeded login')
                return True
        return False

    def _is_login_page(self):
        """
        ログインページかどうかを判定する
        """
        return self.driver.current_url.startswith(self.LOGIN_URL)

    def _is_login_error(self):
        """
        ログインエラーかどうかを判定する
        @return ログインエラーの場合に True を返す
        """
        elements = self.driver.find_elements_by_css_selector('div.yregertxt > h2.yjM')
        return self._is_login_page() and len(elements) != 0

    def _is_image_captcha(self):
        """
        画像キャプチャに引っかかっているかどうかを取得する
        @return 画像キャプチャをもとめられている場合に True を返す
        """
        result = self.driver.current_url.startswith(self.LOGIN_URL)
        result = result and self.driver.title == '文字認証を行います。 - Yahoo! JAPAN'
        if result:
            names = []
            for input_ in self.driver.find_element_by_tag_name('input'):
                names.append(input_['name'])
            checks = [
                'captchaCdata',
                'captchaMultiByteCaptchaId',
                'captchaView',
                'captchaClassInfo',
                'captchaAnswer'
            ]
            for check in checks:
                result = result and check in names
                if not result:
                    return result
        return result

    def _show_image_captcha(self):
        """
        画像キャプチャを表示する
        @return 画像の表示に成功した場合に True を返す
        """
        file = io.BytesIO(request.urlopen(self.driver.find_element_by_id(
            'captchaV5MultiByteCaptchaImg')['src']).read())
        base_image = Image.open(file)
        base_image = base_image.convert('RGBA')
        show_image = Image.new(
            'RGBA', base_image.size, (0xFF, 0xFF, 0xFF, 0x0))
        _width, _height = base_image.size
        for _point_x in range(_width):
            for _point_y in range(_height):
                _pixel = base_image.getpixel((_point_x, _point_y))
                if _pixel != (0, 0, 0, 0):
                    show_image.putpixel((_point_x, _point_y), _pixel)
        show_image.show()
        return True

    def _is_required_one_time_password(self):
        """
        ワンタイムパスワードを求められているかを確認する
        """
        return self.driver.current_url.startswith(self.ONE_TIME_PASSWORD_URL)
