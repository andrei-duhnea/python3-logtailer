#!/usr/bin/env python
from socketserver import StreamRequestHandler, TCPServer
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')


class EchoHandler(StreamRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        msg = str(self.rfile.readline().strip(), 'utf-8')

        cur_thread = threading.current_thread()
        response = "{} {}: {}".format(self.client_address[0], cur_thread.name, msg)

        socketio.emit('my response', {'data': response})


def start_socket_server(ip, port, *, workers=5):
    TCPServer.allow_reuse_address = True
    server = TCPServer((ip, port), EchoHandler)
    for n in range(workers):
        t = threading.Thread(target=server.serve_forever)
        t.daemon = True
        t.start()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('disconnect request')
def disconnect_request():
    emit('my response', {'data': 'Disconnected!'})
    disconnect()


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


if __name__ == '__main__':
    start_socket_server('', 20000)
    socketio.run(app, debug=False)
