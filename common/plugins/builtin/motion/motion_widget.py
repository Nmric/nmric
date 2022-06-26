from common.plugins.core import DisplayPlugin

class MotionWidget(DisplayPlugin):
    def __init__(self):
        description = "The standard control widget to drive the connected machine"
        super().__init__(description=description)

    def render(self) -> str:
        return f"""
    <button type="button" hx-vals='{{"dir":"left", "len":5}}' hx-swap="none" hx-post="/plugin/send/{self.id}">Press</button>
    """

    def do_render(self) -> str:
        return "DO MOTION"