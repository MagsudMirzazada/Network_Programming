import socket
import threading

HOST = "127.0.0.1"
PORT = 1235
HEADERSIZE = 16
DISCONNECT_MESSAGE = "!Disconnect"

def server():
    #Creating and binding socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    print(f'[Server] Server has been assigned to: {HOST} | {PORT}')

    #Listening
    sock.listen(5)
    while True:
        clientsocket, addr = sock.accept()
        thread = threading.Thread(target=handle_client, args=(clientsocket, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1 }')

        # reply = "Welcome to the server"
        # reply = f'{len(msg): < HEADERSIZE}' + reply

def handle_client(clientsocket, addr):
    print(f'[NEW CONNECTION] Client {addr} connected !')

    flag = True
    while flag:
        raw_msg = clientsocket.recv(1024).decode('utf-8')
        if raw_msg:
            msg_length = int(raw_msg[:HEADERSIZE])
            msg = raw_msg[HEADERSIZE:(HEADERSIZE + msg_length)]
            if msg == DISCONNECT_MESSAGE:
                flag = False

            print(f'[{addr[0]}] size: {msg_length} msg: {msg}')
            clientsocket.send("Message received".encode('utf-8'))
            flag = False
    
    clientsocket.close()



def main():
    server()
if __name__ == "__main__":
    main()