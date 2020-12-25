# TAKEN

import argparse
import threading
import pickle
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432
ENCODING = 'utf-8'


class Server:
    def __init__(self):
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        while True:
            try:
                sc, addr = sock.accept()
                thread = threading.Thread(
                    target=self.handler, args=(sc, addr,))
                thread.start()
            except KeyboardInterrupt:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

    def handler(self, sc, addr):
        try:
            time, size = sc.recv(256).decode(ENCODING).split('$')
            sc.send(b'')
            obj = sc.recv(int(size))
            print(f"I recieved message at {time}")
            finalObj = pickle.loads(obj)
            decrText = self.decrypt(finalObj.text)
            reply = str.encode("$".join([str(datetime.now()), decrText]), encoding=ENCODING)
            sc.send(reply)

        finally:
            sc.close()
            print()

    def decrypt(self, data):
        xorKey = 'P'
        length = len(data)
        for i in range(length):
            data = (data[:i] +
                    chr(ord(data[i]) ^ ord(xorKey)) +
                    data[i + 1:])
        return data


class Text:
    def __init__(self, key, text):
        self.text = self.encrypt(text, key)

    def encrypt(self, data, key):
        xorKey = key
        length = len(data)
        for i in range(length):
            data = (data[:i] +
                    chr(ord(data[i]) ^ ord(xorKey)) +
                    data[i + 1:])
        return data


class Client:
    def __init__(self):
        self.obj = Text("P", "plaintext")
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        pickleObj = pickle.dumps(self.obj)
        header = "$".join([str(datetime.now()), str(len(pickleObj))])
        sock.send(header.encode(ENCODING))
        sock.recv(1)
        sock.send(pickleObj)
        time, text = sock.recv(len(self.obj.text) + 58).decode(ENCODING).split('$')
        print(f"Time when reply from server was recieved: {time}")
        print(f"Text is: '{text}'")


def main():
    parser = argparse.ArgumentParser(description='Send URL to the server')
    parser.add_argument('mode', choices=('server', 'client'),
                        help='Mode of running terminal')
    args = parser.parse_args()
    if args.mode == 'server':
        serverObj = Server()
    elif args.mode == 'client':
        clientObj = Client()


if __name__ == "__main__":
    main()
