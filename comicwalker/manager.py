# --- coding: utf-8 ---
"""
comicwalker の操作を行うためのクラスモジュール

https://github.com/YunzheZJU/ComicWalkerWalker
"""

import json
import os
import struct
from manager import AbstractManager


class Manager(AbstractManager):
    """
    comicwalker の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for comicwalker capturing.
        @param driver selenium instance
        """
        super().__init__(driver, config, directory, prefix)

        self.cid = directory[directory.rfind('/') + 1:]
        """
        cid TODO ad-hoc
        """

    def start(self, url=None):
        """
        Starts automatic screenshots of pages.
        @return an error message if the error occurs, or True if it succeeds
        """
        session = self._get_session()

        self._fetch_episode(session, self.directory, self.cid)

        return True

    @staticmethod
    def _generate(key):
        result = []
        for i, k in enumerate(key):
            code = ord(k)
            code = code - 87 if code >= 97 else code - 48
            if i % 2 == 0:
                result.append(code * 16)
            else:
                result[(i - 1) // 2] += code
        return result

    def _fetch_page(self, session, title, page, count):
        # pid = page['id']
        fn = os.path.join(title, '%03d' % count + self._get_extension())
        with open(fn, 'wb') as f:
            url = page['meta']['source_url']
            key = Manager._generate(page['meta']['drm_hash'][:16])
            resp = session.get(url, stream=True, timeout=30)
            for i, c in enumerate(resp.content):
                f.write(struct.pack('B', c ^ key[i % 8]))

    def _fetch_episode(self, session, title, cid):
        resp = session.get('https://ssl.seiga.nicovideo.jp/api/v1/comicwalker/episodes/' + cid + '/frames', timeout=30)
        frame = json.loads(resp.text)['data']['result']
        self._set_total(len(frame))
        for i, page in enumerate(frame):
            self._fetch_page(session, title, page, i)
            self.pbar.update(1)
            self._sleep()
