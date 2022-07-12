import sqlite3
import os
import sys
from pathlib import Path
from inspect import getsourcefile

import zmq
from flask import render_template, request, jsonify, current_app

import common.plugins.core.plugin_manager as pm
from common.db import get_db_connection
from webclient import app
from webclient.display.layout import Layout
from common.plugins.core import DisplayPlugin


# pm.init(pm.PluginManager("app.plugins.builtin"))
HOST = "127.0.0.1"
PORT = 6668
TASK_SOCKET = zmq.Context().socket(zmq.REQ)
TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))


@app.route("/", methods=["GET"])
def home() -> str:
    # TASK_SOCKET.send_string("blaat")
    # results = TASK_SOCKET.recv_string()
    # print("RESULT: ", results)

    # conn = get_db_connection()

    # user = conn.execute("SELECT * from users").fetchone()
    # s = current_app.pm_builtin.plugins[1].render()
    # print(os.path.dirname(getsourcefile(lambda:0)))
    l = Layout()
    layout_html = l.generate()
    # return "TEST " + s + " by " + user["username"]
    return render_template("base.html", element_layout=layout_html)


# @app.route("/plugin/render/<plugin_id>", methods=["GET"])
# def plugin_render(plugin_id: str) -> str:
#     """
#     Render the html of a plugin
#     """
#     # determine if the given ID matches any DisplayWidget plugins
#     plugins = current_app.plugin_manager.get_plugins(DisplayPlugin)

#     if plugin_id in plugins:
#         return plugins[plugin_id].render()
#     else:
#         return "N/A"

# @app.route("/plugin/send/<plugin_id>", methods=["POST"])
# def plugin_send(plugin_id: str) -> str:
#     """
#     Send data without any sort of confirmation
#     """

#     print(plugin_id)
#     print(dict(request.form))
#     print("DIR ",request.args.get("dir"))
#     # did we get valid data?
#     payload = {}
#     if request.is_json:
#         payload = request.get_json()
#         print("payload ", payload)
#     else:
#         return jsonify({"error": "request was not proper"})

#     # determine if the given ID matches any DisplayWidget plugins
#     plugins = current_app.plugin_manager.get_plugins(DisplayPlugin)

#     if plugin_id in plugins:
#         response = plugins[plugin_id].process(payload)
#         return jsonify(response)
#     else:
#         return jsonify({"error": "plugin not found"})
