import zmq
import time
import sys
import os
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv('PORT')

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    if len(sys.argv) > 2:
        global PORT
        PORT = int(sys.argv[2])

    socket.bind(f"tcp://*:{PORT}")
    print(f"SERVER started on port: {PORT}")

    while True:
        msg = socket.recv()
        print(msg)
        time.sleep(1)
        socket.send_string(f"[SERVER] Hi client!")

def client():
    ports = []
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    if len(sys.argv) > 2:
        global PORT
        PORT = int(sys.argv[2])

    socket.connect(f"tcp://localhost:{PORT}")
    ports.append(PORT)

    if len(sys.argv) > 3:
        PORT1 = int(sys.argv[3])
        socket.connect(f"tcp://localhost:{PORT1}")
        ports.append(PORT1)


    for i in ports:
        print(f"Connected to port: {i}")
    print('-'*40)

    z = 0
    while z<10:
        print(f"Sending request {z}")
        socket.send_string(f"[CLIENT] Hi server!")
        msg = socket.recv()
        print(msg)
        z += 1


def main():
    if sys.argv[1] == 'server':
        server()
    elif sys.argv[1] == 'client':
        client()
    else:
        print("INVALID")

if __name__ == '__main__':
    main()