import threading
import socket
users = []

class User:
    def __init__(self, client, name):
        self.client = client
        self.name = name
     
def broad_cast(message):
    for user in users:
        user.client.send(message)

def handle_client(user):
    while True:
        message = user.client.recv(1024).decode('utf-8')

        if message == "_QUIT_":
            message = (f'{user.name} has left the chat room!'.encode('utf-8'))
            broad_cast(message)
            users.remove(user)
            user.client.close()
            break
                
        message = f'{user.name}: {message}'.encode('utf-8')
        broad_cast(message)         

def receive():
    HOST = socket.gethostbyname(socket.gethostname())
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, 5050))
    server.listen()

    while True:

        print('Server is Active.')
        client, address = server.accept()
        name = client.recv(1024).decode('utf-8')
        print(f'{str(address)} has connected.')
        
        message = (f'{name} has joined the chat room!'.encode('utf-8'))
        
        user = User(client, name)
        users.append(user)
        broad_cast(message)

        thread = threading.Thread(target=handle_client, args=(user,))
        thread.start()

if __name__ == "__main__":
    receive()
