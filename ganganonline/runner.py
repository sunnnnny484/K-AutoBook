# --- coding: utf-8 ---
"""
A module for gangan-online runner.
"""

from runner import DirectPageRunner
from ganganonline.manager import Manager


class Runner(DirectPageRunner):
    """
    A class for gangan-online runner.
    https://viewer.ganganonline.com/manga/?chapterId=15502
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)
