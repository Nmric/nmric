from common.plugins.core import DisplayPlugin

class TerminalWidget(DisplayPlugin):
    def __init__(self):
        description = "The standard terminal widget to send g-code to the connected machine"
        super().__init__(description=description)

    def render(self) -> str:
        return "TERMINAL!"