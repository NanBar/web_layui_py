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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode, logger=True, engineio_logger=True)
thread = None
thread_lock = Lock()




@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)



@socketio.on('*')
def catch_all(event, data):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': [event, data], 'count': session['receive_count']})


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.event
def my_ping():
    emit('my_pong')



def run_flask():
    socketio.run(app, host='127.0.0.1', port=5001)  # 指定主机和端口
    # socketio.run(app)


def run_webview():
    webview.create_window('pyweb测试', 'http://127.0.0.1:5001')  # 创建浏览器窗口
    webview.start()  # 启动 pywebview


if __name__ == '__main__':
    multiprocessing.freeze_support()
    flask_process = Process(target=run_flask)
    flask_process.start()
    webview_process = Process(target=run_webview)
    webview_process.start()
    webview_process.join()
    os.kill(flask_process.pid, signal.SIGTERM)
