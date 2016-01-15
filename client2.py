import time
from socket import socket, AF_INET, SOCK_STREAM


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
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socket_send("Client 2 sent: message number " + str(count))
