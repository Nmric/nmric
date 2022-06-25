import time
import zmq


class MachineHandler:
    
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://127.0.0.1:{port}")

    def run(self):
        while True:
            #  Wait for next request from client
            message = self.socket.recv()
            print("Received request: %s" % message)

            #  Do some 'work'
            time.sleep(1)

            #  Send reply back to client
            self.socket.send(b"World")
