# TAKEN
# CONNECTS VIA TCP, COLLECTS IMAGE COUNTS AND LEAF PARAGRAPH ELEMENTS WITH WEB-SCRAPPING VIA BEAUTIFULSOUP

import sys
from bs4 import BeautifulSoup
from termcolor import colored
import socket
import requests
import argparse
import threading

HOST = "127.0.0.1"
PORT = 65430
ENCODING = 'utf-8'


class Server:
    def __init__(self):
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        print(
            f"{colored('[SERVER]', 'green')} {colored('has started on ', 'yellow')}" +
            f"{colored(str(HOST) + ':' + str(PORT), 'blue')}")
        while True:
            try:
                sc, addr = sock.accept()
                thread = threading.Thread(
                    target=self.handler, args=(sc, addr,))
                thread.start()
            except KeyboardInterrupt:
                print(
                    colored(f"TERMINAL KILLED!", 'red'))
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

    def handler(self, sc, addr):
        try:
            fullUrl = (sc.recv(128)).decode(ENCODING)
            url = 'https://' + \
                fullUrl.split('//')[len(fullUrl.split('//')) - 1]
            print(
                f"{colored('Connected to', 'yellow')} {colored(str(addr[0]) + ':' + str(addr[1]), 'blue')} " +
                f"{colored('and processing', 'yellow')} {colored(url, 'red')}")
            content = requests.get(url).content
            soup = BeautifulSoup(content, "html.parser")
            soup.prettify()
            pList = soup.find_all("p")
            leafCounter = 0
            for pElement in pList:
                if not pElement.find_all("p"):
                    leafCounter += 1
            imageCounter = len(soup.find_all("img"))
            finalResult = str(imageCounter) + ',' + \
                str(leafCounter) + ',' + str(url)
            sc.send(finalResult.encode(ENCODING))
        finally:
            sc.close()
            print(
                colored(f"Disconnected from {colored(str(addr[0]) + ':' + str(addr[1]), 'blue')}", 'red'))
            print()


class Client:
    def __init__(self, url):
        self.url = url
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(self.url.encode(ENCODING))
        data = sock.recv(128)
        imgCount, leafCount, url = data.decode(ENCODING).split(',')
        print(
            f"{colored(url, 'red')} {colored('has', 'yellow')} " +
            f"{colored(imgCount + ' images', 'green')} " +
            f"{colored('and', 'yellow')} " +
            f"{colored(leafCount + ' leaf paragraphs', 'blue')}")


def main():
    parser = argparse.ArgumentParser(description='Send URL to the server')
    parser.add_argument('mode', choices=('server', 'client'),
                        help='Mode of running terminal')
    if 'client' in sys.argv:
        parser.add_argument('-p', type=str, help='URL of website')
    args = parser.parse_args()
    if args.mode == 'server':
        serverObj = Server()
    elif args.mode == 'client':
        clientObj = Client(args.p)
    else:
        parser.error(
            colored(f"Enter one argument of {colored('{server, client}', 'blue')}", "red"))


if __name__ == "__main__":
    main()