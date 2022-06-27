import time
from typing import Dict

from flask import Flask, g
from flask_sock import Sock

from common.plugins.core.plugin_manager import PluginManager
from common.plugins.core import DisplayPlugin


def echo_socket(ws):
    result = ""
    i = 0
    n = 0
    while True:
        i += 1
        if i > 0:
            i = 0
            n += 1
            result += f"<b>{n}</b><br>" 
            # data = ws.receive()
            print("ECHO ", n)
            ws.send(f"<div id='terminal_output' hx-swap-oob='true'>{result}</div>")
        time.sleep(2)

class WebApp(Flask):
    plugin_manager = PluginManager(["common.plugins.repo.builtin", "common.plugins.repo.community"])
    # pm = None

    # def __init__(self):
        # self.register_plugin_routes()

    def register_plugin_routes(self, sock: Sock = None) -> None:

        if sock:  # keep the websocket interface around
            self.sock = sock

        # dynamically register endpoints for plugins
        plugins = self.plugin_manager.get_plugins(DisplayPlugin)  # type: Dict[str, DisplayPlugin]
        for plugin in plugins.values():
            # print("VIEW ",plugin.id)
            self.route(f"/plugins/render/{plugin.id}", methods=["GET"], endpoint=f"render_{plugin.id}")(plugin.render)
            self.route(f"/plugins/post/{plugin.id}", methods=["POST"], endpoint=f"post_{plugin.id}")(plugin.receive)
    
            # websocket endpoints
            self.sock.route(f"/plugins/stream/{plugin.id}", endpoint=f"stream_{plugin.id}")(plugin.stream)