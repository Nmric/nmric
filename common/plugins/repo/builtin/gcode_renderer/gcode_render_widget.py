from common.plugins.core import DisplayPlugin

class GcodeRenderer(DisplayPlugin):
    def __init__(self):
        description = "Visualize the loaded gcode instructions"
        super().__init__(description=description)

    def render(self) -> str:
        return "GCODE!"
