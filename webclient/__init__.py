import zmq
import time
from multiprocessing import Process

import flask
from flask import Flask, g
from flask_sock import Sock

from .webapp import WebApp


HOST = "127.0.0.1"
PORT = 6668

    
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

app = WebApp(__name__)
sock = Sock(app)

app.register_plugin_routes(sock)

# print(app.url_map)

# app.config["DATABASE_URI"] = 'sqlite:///persistence.db'
#app.config["SQLALCHEMY_ECHO"] = False
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# pm = PluginManager("common.plugins.builtin")
# app.pm = pm
#db = SQLAlchemy(app)

from webclient import views
from webclient import models

