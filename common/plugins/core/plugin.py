import inspect
import os
# from pathlib import Path

from flask import send_from_directory, Response

class Plugin:

    def __init__(self, description = "N/A"):
        self.description = description
        self.id = self.get_id()
        self.plugin_path = self.get_plugin_path()

    def get_id(self) -> str:
        """
        To make plugins easy to identify we generate a ID based on the location of the plugin in the repo
        
        :returns: unique ID for this plugin
        """
        full_class_path = str(self.get_plugin_path())
        root_path = os.path.join(os.getcwd(), "common", "plugins", "repo")

        return full_class_path.replace(root_path, "").replace("/", ".").replace("\\", ".")[1:]
        
    def get_plugin_path(self) -> str:
        return os.path.dirname(inspect.getfile(self.__class__))

    def initialize(self):
        pass

    def get_static_file(self, filename) -> Response:
        return send_from_directory(str(os.path.join(self.plugin_path, "static")), filename)