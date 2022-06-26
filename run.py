import logging.config
import sqlite3
from os.path import exists
from time import sleep

# from flask_socketio import SocketIO
from flask_sock import Sock

from webclient import app

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        'weblogger': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)

    logger = logging.getLogger("weblogger")
    logger.info("Starting Numrc")

    logger.info("Checking for database")

    if not exists("persistence.db"):
        logger.warning("Database does not exist; generating new instance")
        connection = sqlite3.connect('persistence.db')

        with open('persistence.sql') as f:
            connection.executescript(f.read())

            cur = connection.cursor()

            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        ('Menno', 'test')
                        )

            connection.commit()
            connection.close()
    else:
        logger.info("Database was found")

    # create database if none exists
    # socketio = SocketIO(app, cors_allowed_origins="*",source="ws",namespace="/")
    sock = Sock(app)
    
    # @sock.route('/ws')
    def echo_socket(ws):
        result = ""
        i = 0
        n = 0
        while True:
            i += 1
            if i > 100000000:
                i = 0
                n += 1
                result += f"<b>{n}</b><br>" 
                # data = ws.receive()
                print(n)
                ws.send(f"<div id='terminal_output' hx-swap-oob='true'>{result}</div>")
        # while not ws.closed:
        #     message = ws.receive()
        #     print(message)
        #     ws.send(message)
    sock.route("/ws")(echo_socket)  # add these dynamically for plugins

    # @socketio.on('message')
    # def handle_message(data):
    #     print('received message: ' + data)

    # socketio.run(app)
    app.run()
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()
