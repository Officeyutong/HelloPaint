#! /usr/bin/env python3.6

from board_manager import BoardManager
from global_objs import config, VARS
from datetime import timedelta

from flask_socketio import SocketIO
import flask
import os
import threading
app = flask.Flask("HelloPaint")
app.secret_key = config.SESSION_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

socket = SocketIO(app)
from global_objs import VARS



def save_thread():
    print("Saving...")
    app.boards.save_to_file(config.SAVE_FILE)
    global saver
    saver = threading.Timer(config.SAVE_INTERVAL, save_thread)
    saver.start()


saver = threading.Timer(config.SAVE_INTERVAL, save_thread)


@app.before_first_request
def init():
    app.boards = BoardManager()
    if os.path.exists(config.SAVE_FILE):
        app.boards.load_from_file(config.SAVE_FILE)
    saver.start()

from routes import *
from views import *

if __name__ == "__main__":
    socket.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)
    print("Closing....")
    # saver.cancel()
    # app.boards.save_to_file(config.SAVE_FILE)
    exit(0)
