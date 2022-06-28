import time

import zmq
from flask import make_response, Response

from common.plugins.core import DisplayPlugin

class TerminalWidget(DisplayPlugin):
    def __init__(self):
        description = "The standard terminal widget to send g-code to the connected machine"
        super().__init__(description=description)

    def render(self) -> Response:
        template = """
        <div hx-ws="connect:/plugins/stream/builtin.terminal">
            <div id="terminal_output">
                ...
            </div>
            <form hx-ws="send">
                <input name="terminal_command">
            </form>
        </div>
        """

        return make_response(template, 200)

    def stream(self, websocket) -> str:
        machine_host = "127.0.0.1"
        machine_port = 6668

        socket = zmq.Context().socket(zmq.REQ)
        socket.connect('tcp://{}:{}'.format(machine_host, machine_port))
        socket.setsockopt(zmq.RCVTIMEO, 2000)

        while True:
            i += 1
            if i > 0:
                i = 0
                n += 1
                result += f"<b>{n}</b><br>" 
                # data = ws.receive()
                print("ECHO ", n)
                websocket.send(f"<div id='terminal_output' hx-swap-oob='true'>{result}</div>")
            time.sleep(2)

    # def stream(self, ws) -> str:
    #     result = ""
    #     i = 0
    #     n = 0
    #     while True:
    #         i += 1
    #         if i > 0:
    #             i = 0
    #             n += 1
    #             result += f"<b>{n}</b><br>" 
    #             # data = ws.receive()
    #             print("ECHO ", n)
    #             ws.send(f"<div id='terminal_output' hx-swap-oob='true'>{result}</div>")
    #         time.sleep(2)
