import inspect
import os
from pathlib import Path


class Plugin:

    def __init__(self, description = "N/A"):
        self.description = description
        self.id = self.get_id()

    def get_id(self) -> str:
        """
        To make plugins easy to identify we generate a ID based on the location of the plugin in the repo
        
        :returns: unique ID for this plugin
        """
        root_path = os.path.join(os.getcwd(), "common", "plugins")
        full_class_path = str(Path(inspect.getmodule(self).__file__))

        full_id = full_class_path.replace(root_path, "").replace(".py", "").replace("/", ".").replace("\\", ".")[1:]
        return ".".join(full_id.split(".")[1:-1])  # remove the first and last part (which don't contain usefull info)
        
    def initialize(self):
        pass
