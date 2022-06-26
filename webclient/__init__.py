import zmq
import time
from multiprocessing import Process

from common.plugins.core.plugin_manager import PluginManager
from common.plugins.core import DisplayPlugin
from flask import Flask, g

HOST = "127.0.0.1"
PORT = 6668

class WebClient(Flask):
    pm_builtin = PluginManager("common.plugins.builtin")
    pm_repo = PluginManager("common.plugins.repo")
    # pm = None

    # def __init__(self):
        # self.register_plugin_routes()

    def register_plugin_routes(self) -> None:

        plugins = self.pm_builtin.get_plugins(DisplayPlugin)
        for plugin in plugins.values():
            view_func = plugin.do_render
            print("VIEW ",plugin.id)
            self.route(f"/plugins/render/{plugin.id}", methods=["GET"], endpoint=f"{plugin.id}_do_render")(view_func)
    
    
# class Machine(Process):
#     _stopped = False
#     _count = 0
    
#     def __init__(self):
#         super(Machine, self).__init__()

#         print("Machine init")
#         self._context = zmq.Context()
#         self._socket = self._context.socket(zmq.REP)

#         self._socket.bind('tcp://{}:{}'.format(HOST, PORT))
#         self._socket.setsockopt(zmq.RCVTIMEO, 500)
#     def run(self):
#         print("started socket")
#         while not self._stopped:
#             message = self._socket.recv()
#             print("MSG ", message)
#             if self._count % 1000000 == 0:
#                 a = 1
#                 # print("COUNT: ", self._count)
#                 # ev = self._socket.poll(1000)
#                 # if ev:
#                     # print("EVENT: ", ev)
#                     # rec = self._socket.recv_json()
#                     # self._socket.send_json({"response": "ok", "payload": self._count})
#             self._count += 1

# machine = Machine()
# machine.start()

app = WebClient(__name__)
app.register_plugin_routes()

app.config["DATABASE_URI"] = 'sqlite:///sqlite.db'
#app.config["SQLALCHEMY_ECHO"] = False
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# pm = PluginManager("common.plugins.builtin")
# app.pm = pm
#db = SQLAlchemy(app)

from webclient import views
from webclient import models

