from .plugin import Plugin

from typing import Dict


class DisplayPlugin(Plugin):

    def __init__(self, **args):
        super().__init__(args)

    def render(self):
        pass

    def triggered(self, data: Dict):
        pass

    def respond(self, data: Dict):
        pass