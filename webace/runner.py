# --- coding: utf-8 ---
"""
A module for web-ace runner.
"""

from runner import DirectPageRunner
from webace.manager import Manager


class Runner(DirectPageRunner):
    """
    A class for web-ace runner.
    https://web-ace.jp/youngaceup/contents/1000053/episode/1092/
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)
