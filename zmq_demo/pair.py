import zmq
import time
import argparse
import os
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv('PORT')

def server():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind(f"tcp://*:{PORT}")

    while True:
        socket.send_string("Server")
        msg = socket.recv()
        print(msg)

        time.sleep(1)

def client():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://localhost:{PORT}")

    while True:
        msg = socket.recv()
        print(msg)
        socket.send_string('CLIENT')

        time.sleep(1)

def main():
    mode_args = argparse.ArgumentParser()
    mode_args.add_argument('mode', choices=('server', 'client'))
    args = mode_args.parse_args()

    if args.mode == 'server':
        server()
    elif args.mode == 'client':
        client()

if __name__ == '__main__':
    main()
