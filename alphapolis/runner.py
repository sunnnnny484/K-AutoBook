# --- coding: utf-8 ---
"""
A module for alpha-police capturing.
"""

from runner import AbstractRunner
from alphapolis.manager import Manager


class Runner(AbstractRunner):
    """
    A class for alpha-police capturing.
    """

    def run(self):
        """
        Proceeds alpha-police runner.
        """
        destination = self.get_output_dir()
        manager = Manager(self.driver, None, destination)
        manager.start(self.url)
