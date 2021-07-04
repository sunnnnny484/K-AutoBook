# --- coding: utf-8 ---
"""
ebookjapanの設定モジュール
"""

from config import SubConfigWithCookie


class SubConfig(SubConfigWithCookie):
    """
    設定情報を管理するためのクラス
    """

    def __init__(self):
        """
        設定情報を管理するためのコンストラクタ
        """
        super().__init__()

        self.blank_check_excludes = set()
        """
        black page checking excludes pages, negative number or zero means (total - 1 + negative_number)
        """
        self.blank_check_giveup = 11
        """
        black page checking give up times
        11 is larger than retry times, means never give up, means retry error stop downloading.
        """

    def update(self, data):
        """
        設定情報を更新する
        @param data 更新するデータ
        """
        super().update(data)

        if 'blank_check_excludes' in data:
            self.blank_check_excludes = eval(data['blank_check_excludes'])
        if 'blank_check_giveup' in data:
            self.blank_check_giveup = data['blank_check_giveup']
