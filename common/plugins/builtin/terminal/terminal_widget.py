from common.plugins.core import DisplayPlugin

class TerminalWidget(DisplayPlugin):
    def __init__(self):
        description = "The standard terminal widget to send g-code to the connected machine"
        super().__init__(description=description)

    def render(self) -> str:
        return """
        <div hx-ws="connect:/ws">
            <div id="terminal_output">
                ...
            </div>
            <form hx-ws="send:submit">
                <input name="terminal_command">
            </form>
        </div>
        """