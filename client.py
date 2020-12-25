import socket

HOST = "127.0.0.1"
PORT = 1235
HEADERSIZE = 16
DISCONNECT_MESSAGE = "!Disconnect"
CLIENT_IP = ''

def client():
    #Creating socket and connecting
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f'[CLIENT] Client has been assigned to: {sock.getsockname()[0]} | {sock.getsockname()[1]}')

    msg1 = "MagsudMirzazaDa"
    msg2 = "Hello World"
    send(sock, msg1)
    input()
    send(sock, msg2)
    input()

    sock.close()

def send(sock, msg):
    msg_content = msg.encode('utf-8')
    msg_length = str(len(msg_content)).encode('utf-8')

    final_msg = msg_length + b' '*(HEADERSIZE - len(msg_length)) + msg_content
    sock.send(final_msg)

    print(sock.recv(1024).decode('utf-8'))



def main():
    client()
if __name__ == "__main__":
    main()