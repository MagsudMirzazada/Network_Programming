import zmq
import time
import sys
import random
import os
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv('PORT')

def pub():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = PORT

    socket.bind(f"tcp://*:{port}")
    print(f"SERVER started on port: {port}")
    print('-'*40)

    while True:
        topic = random.randrange(9999, 10005)
        msg = 'NewYork' if topic==10001 else 'Somewhere'
        print(msg)
        socket.send_string(f"{topic} {msg}")
        time.sleep(1)


def sub():
    ports = []
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = PORT
    socket.connect(f"tcp://localhost:{port}")
    ports.append(port)

    if len(sys.argv) > 3:
        port1 = int(sys.argv[3])
        socket.connect(f"tcp://localhost:{port1}")
        ports.append(port1)
    
    for i in ports:
        print(f"Connected to port: {i}")
    print('-'*40)

    # Filter
    topicfilter = os.getenv('topicfilter')
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while True:
        raw_msg = socket.recv()
        topic, msg = raw_msg.split()
        print(f"{topic}: {msg}")
        


def main():
    if sys.argv[1] == 'publisher':
        pub()
    elif sys.argv[1] == 'subscriber':
        sub()
    else:
        print('INVALID')
 
if __name__ == '__main__':
    main()