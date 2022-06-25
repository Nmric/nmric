import inspect
import os
from pathlib import Path


class Plugin:

    def __init__(self, description = "N/A"):
        self.description = description
        self.id = self.get_id()

    def get_id(self) -> str:
        root_path = os.path.join(os.getcwd(), "common", "plugins")
        full_class_path = str(Path(inspect.getmodule(self).__file__))

        return full_class_path.replace(root_path, "").replace(".py", "").replace("/", ".")[1:]
        
    def initialize(self):
        pass
