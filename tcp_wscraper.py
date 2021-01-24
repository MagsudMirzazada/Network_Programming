# M
# # CONNECTS VIA TCP, COLLECTS LEAF DIV ELEMENTS WITH WEB-SCRAPPING VIA BEAUTIFULSOUP

import socket
import threading
import requests
from bs4 import BeautifulSoup
import argparse
import sys
from termcolor import colored
import pickle

HOST = '127.0.0.1'
PORT = 5001
MAX_BYTES = 65535
HEADER_SIZE = 8

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError(f'''was expecting {length} bytes, but only received {len(data)} bytes
                            before socket closed''')
        data += more
    return data

def make_message(msg):
    message = f"{len(msg):<8}{msg}"
    message = message.encode('utf-8')
    return message

class Server():
    def __init__(self):
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        print(colored('[SERVER]', 'green'), colored('started on', 'yellow'), colored(str(HOST) + ':' + str(PORT), 'blue'))
        while True:
            try:
                clientsocket, addr = sock.accept()
                thread =threading.Thread(target=self.handler, args=(clientsocket, addr,))
                thread.start()
            except KeyboardInterrupt:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

    def handler(self, clientsocket, addr):
        try:
            length = (recv_all(clientsocket, HEADER_SIZE)).decode('utf-8')
            print(f"Message length is {length}")
            raw_url = (recv_all(clientsocket, int(length))).decode('utf-8')
            # sssssssss
            # raw_url = (clientsocket.recv(256)).decode('utf-8')
            url = "https://" + raw_url
            print(
                f"{colored('Connected to', 'yellow')} {colored(str(addr[0]) + ':' + str(addr[1]), 'blue')} " + 
                f"{colored('and processing', 'yellow')} {colored(url, 'red')}"
            )

            res = requests.get(url).content
            soup = BeautifulSoup(res, 'html.parser')
            soup.prettify()
            paragraphs = soup.find_all('div')
            
            #for leaf paragraphs
            cont = 0
            for para in paragraphs:
                if not para.find_all('p'):
                    cont += 1
            result = str(cont) + ',' + str(url)
            
            # #for all paragraphs
            # result = str(len(paragraphs)) + ',' + str(url)
            
            '''
            #test
            cont = list()
            for para in paragraphs:
                if not para.find_all('p'):
                    cont.append(para.string)
            result = pickle.dumps(cont)
            clientsocket.send(result)
            #test finish
            '''

            data = make_message(result)
            clientsocket.send(data)
        finally:
            clientsocket.close()
            print(colored(f"Disconnected from {colored(str(addr[0]) + ':' + str(addr[1]), 'blue')}", "yellow"))
            print()


class Client():
    def __init__(self, url):
        self.url = url
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        data = make_message(self.url)
        sock.send(data)
        sock.shutdown(socket.SHUT_WR)

        length = (recv_all(sock, HEADER_SIZE)).decode('utf-8')

        reply = (recv_all(sock, int(length))).decode('utf-8')

        #sssss
        #sock.send(self.url.encode('utf-8'))
        #data = (sock.recv(256)).decode('utf-8')
        para, url = reply.split(',')
        print(
            f"{colored(url, 'red')} {colored('has', 'yellow')} {colored(para, 'red')} {colored('divs', 'yellow')}"
        )

        # #test
        # data = sock.recv(256)
        # res = pickle.loads(data)
        # print(res)
        # #test finish

def main():
    #print(threading.enumerate())
    
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('server', 'client'))
    if 'client' in sys.argv:
        parser.add_argument('-u', type=str, help='URL of website')
    args = parser.parse_args()

    if args.mode == 'server':
        serverObj = Server()
    if args.mode =='client':
        clientObj = Client(args.u)
    else:
        parser.error(colored('Invalid syntax', 'red'))

if __name__ == '__main__':
    main()