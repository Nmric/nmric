import json
import serial
import time
import zmq


class MachineHandler:
    
    def __init__(self, port):
        self.request_port = 6668
        self.broadcast_port = 6669

        self.context = zmq.Context()
        self.request_socket = self.context.socket(zmq.REP)
        self.request_socket.bind(f"tcp://127.0.0.1:{self.request_port}")

    def connect(self, device, baud_rate):
        self.serial = serial.Serial(device, baud_rate)

    def run(self):
        """
        Input loop: 
        """
        while True:
            #  Wait for next request from client
            message = self.request_socket.recv()
            print("Received request: %s" % message)

            #  Do some 'work'
            # time.sleep(1)

            #  Send reply back to client
            self.request_socket.send(b"World")
