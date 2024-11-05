import multiprocessing
from multiprocessing import Process
import threading
from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_cors import CORS
import webview
import os
import signal

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
from engineio.async_drivers import eventlet

async_mode = "eventlet"  # 显式指明异步库

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode, logger=True, engineio_logger=True)
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})


@app.route('/')
def index():
    return app.send_static_file('index.html')
    # return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


def run_flask():
    socketio.run(app, host='127.0.0.1', port=5000)  # 指定主机和端口
    # socketio.run(app)


def run_webview():
    webview.create_window('pyweb测试', 'http://127.0.0.1:5000')  # 创建浏览器窗口
    webview.start()  # 启动 pywebview


if __name__ == '__main__':
    app.run()
    multiprocessing.freeze_support()
    flask_process = Process(target=run_flask)
    flask_process.start()
    webview_process = Process(target=run_webview)
    # webview_process.start()
    webview_process.join()
    os.kill(flask_process.pid, signal.SIGTERM)
