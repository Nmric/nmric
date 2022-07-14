import sqlite3
from os.path import exists

from webclient import app
from common.logger import log


if __name__ == "__main__":
    log.info("Starting Numrc")

    log.info("Checking for database")

    if not exists("persistence.db"):
        log.warning("Database does not exist; generating new instance")
        connection = sqlite3.connect('persistence.db')

        with open('db_schema/persistence.sql') as f:
            connection.executescript(f.read())

            cur = connection.cursor()

            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        ('Menno', 'test')
                        )

            connection.commit()
            connection.close()
    else:
        log.info("Database was found")

    app.run()
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()
