from .plugin import Plugin

from typing import Dict


class DisplayPlugin(Plugin):

    def __init__(self, **args):
        super().__init__(args)

    def render(self) -> str:
        return "<b>N\A</b>"

    def triggered(self):
        pass

    def receive(self):
        pass

    def stream(self):
        pass
