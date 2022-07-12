import time
from typing import Dict

from flask import Flask, g
from flask_sock import Sock

from common.plugins.core.plugin_manager import PluginManager
from common.plugins.core import DisplayPlugin


class WebApp(Flask):
    plugin_manager = PluginManager(["common.plugins.repo.builtin", "common.plugins.repo.community"])

    # def __init__(self):
        # self.register_plugin_routes()

    def register_plugin_routes(self, sock: Sock = None) -> None:

        if sock:  # keep the websocket interface around
            self.sock = sock

        # dynamically register endpoints for plugins
        plugins = self.plugin_manager.get_plugins(DisplayPlugin)  # type: Dict[str, DisplayPlugin]
        for plugin in plugins.values():
            self.route(f"/plugins/render/{plugin.id}", methods=["GET"], endpoint=f"render_{plugin.id}")(plugin.render)
            self.route(f"/plugins/post/{plugin.id}", methods=["POST"], endpoint=f"post_{plugin.id}")(plugin.receive)
            self.route(f"/plugins/static/{plugin.id}/<path:filename>",
                       endpoint=f"static_{plugin.id}")(plugin.get_static_file)
    
            # websocket endpoints
            self.sock.route(f"/plugins/stream/{plugin.id}", endpoint=f"stream_{plugin.id}")(plugin.stream)