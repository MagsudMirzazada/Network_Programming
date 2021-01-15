import zmq
import time
import sys
import random
import os
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv('PORT')
TERMINATION_KEY = os.getenv('TERMINATION_KEY')
WORKER_NUM = os.getenv('WORKER_NUM')

def ventilator():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)

    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = PORT
    socket.bind(f"tcp://*:{port}")
    print(f"SERVER started on port: {port}")
    print('-'*40)

    z = 1
    while z<10:
        msg = {'num': z}
        print(msg)
        socket.send_json(msg)
        time.sleep(1)
        z += 1
    # Sending termination
    for i in range(int(WORKER_NUM)):
        socket.send_json({'num': TERMINATION_KEY})
        
def worker():
    worker_id = random.randrange(100, 10000)
    context = zmq.Context()

    # Pulling from
    socket_from = context.socket(zmq.PULL)
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = PORT
    socket_from.connect(f"tcp://localhost:{port}")
    print(f"Receiving from port: {port}")

    # Pushing to
    socket_to = context.socket(zmq.PUSH)
    if len(sys.argv) > 3:
        port1 = int(sys.argv[3])
    else:
        port1 = PORT
    socket_to.connect(f"tcp://localhost:{port1}")
    print(f"Sending to port: {port1}")
    print('-'*40)

    while True:
        msg = socket_from.recv_json()
        data = msg['num']
        result = {'worker': worker_id, 'num': data}
        print(result)
        socket_to.send_json(result)
        if  msg['num'] == TERMINATION_KEY:
            break

def sink():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = PORT
    socket.bind(f"tcp://*:{port}")
    print(f"SINK binded to port: {port}")
    print('-'*40)

    while True:
        msg = socket.recv_json()
        if  msg['num'] == TERMINATION_KEY:
            break
        print(msg)


def main():
    if sys.argv[1] == 'ventilator':
        ventilator()
    elif sys.argv[1] == 'worker':
        worker()
    elif sys.argv[1] == 'sink':
        sink()
    else:
        print('INVALID')

if __name__ == '__main__':
    main()