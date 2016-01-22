#!/usr/bin/env python
import json
from socketserver import StreamRequestHandler, TCPServer
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from flask.ext.bootstrap import Bootstrap, StaticCDN

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

Bootstrap(app)

app.extensions['bootstrap']['cdns']['jquery'] = StaticCDN()
app.extensions['bootstrap']['cdns']['bootstrap'] = StaticCDN()


class EchoHandler(StreamRequestHandler):

    def handle(self):
        json_msg = json.loads(str(self.rfile.readline(), 'utf-8'))

        # append IP info
        json_msg['ip'] = self.client_address[0]

        socketio.emit('my response', json_msg)


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
    emit('my response', {'msg': message['data']})


@socketio.on('disconnect request')
def disconnect_request():
    emit('my response', {'msg': 'Disconnected!'})
    disconnect()


@socketio.on('connect')
def test_connect():
    emit('my response', {'msg': 'Flask Connected'})


if __name__ == '__main__':
    start_socket_server('', 20000)
    socketio.run(app, debug=False)
