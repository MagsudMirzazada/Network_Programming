import socket
import argparse


class Server:
    def __init__(self):
        self.interface = '192.168.0.101'
        self.port = 1616
    
    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((self.interface, self.port))
        soc.listen(5)
        print('Listening at', soc.getsockname())
        print(soc.getsockname()[0])

        while True:
            print("Waiting for connection...")
            client_socket, addr = soc.accept()

            print(f'We have accepted connettion from: {addr}')
            print(f'Client\'s Socket Name: {client_socket.getsockname()}')

            message = client_socket.recv(1024)
            print(f'Incoming octet message: {repr(message)}')

            client_socket.sendall(b'Farewell, client')

            client_socket.close()
            print(' Reply sent, socket closed')
#-------------------------------------------------------------------CLIENT----------------------------------------------------------------------------------------
class Client:
    def __init__(self):
        self.interface = '127.0.0.1'
        self.port = 1616
    
    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.interface, self.port))

        print(f'Client has been assigned: {soc.getsockname}')
        soc.sendall(b'Hi there, server')
        reply = soc.recv(1024)
        print(f'The server said: {reply}')
        soc.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    choices = {'server': Server, "client": Client}
    parser = argparse.ArgumentParser(description="Text Service")
    parser.add_argument("role", choices=choices)

    args = parser.parse_args()

    clss = choices[args.role]()
    clss.run()


if __name__ == '__main__':
    main()