import time
from socket import socket, AF_INET, SOCK_STREAM


def follow(the_file):
    the_file.seek(0, 2)
    while True:
        file_line = the_file.readline()
        if not file_line:
            time.sleep(0.1)
            continue
        yield file_line


def socket_send(msg):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect(('localhost', 20000))
        sock.sendall(bytes(msg + "\n", 'utf-8'))
        print('Sent {}'.format(msg.strip()))
    except ConnectionRefusedError:
        print("Error connecting to server.")
    finally:
        sock.close()

if __name__ == '__main__':
    logfile = open('/var/log/system.log', 'r')
    loglines = follow(logfile)
    for line in loglines:
        socket_send(line)
