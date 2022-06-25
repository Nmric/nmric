import logging.config
import sqlite3
from os.path import exists

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
    app.run()

