import socket
import threading
from datetime import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.148.233', 12345))
server.listen(5)

clients = {}
client_threads = {} 

def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sender_username = clients[sender_socket]
                client_socket.send(f"{timestamp} {sender_username}: {message}".encode())
            except:
                continue

def handle_client(client_socket):
    try:
        client_socket.send("Please set your username: ".encode())
        username = client_socket.recv(1024).decode('utf-8').strip()
        if not username:
            username = "Anonymous"
        client_socket.send(f"Your username is set to {username}".encode())
        clients[client_socket] = username

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(message, client_socket)
        
    except:
        del clients[client_socket]
        client_socket.close()
        client_threads[client_socket].set()  # Signal the thread to exit.

def manage_clients():
    while True:
        print("Menu:")
        print("1. List Connected Clients")
        print("2. Ban a Client")
        print("3. Disconnect a Client")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Connected Clients:")
            for username in clients.values():
                print(username)
        elif choice == '2':
            username_to_ban = input("Enter the username to ban: ")
            for client_socket, username in clients.items():
                if username == username_to_ban:
                    client_socket.send("You have been banned.".encode())
                    del clients[client_socket]
                    client_socket.close()
                    client_threads[client_socket].set()  # Signal the thread to exit.
        elif choice == '3':
            username_to_disconnect = input("Enter the username to disconnect: ")
            for client_socket, username in clients.items():
                if username == username_to_disconnect:
                    client_socket.send("You have been disconnected by the server.".encode())
                    del clients[client_socket]
                    client_socket.close()
                    client_threads[client_socket].set()  # Signal the thread to exit.

# Start a thread for managing clients.
management_thread = threading.Thread(target=manage_clients)
management_thread.start()

while True:
    client_socket, client_address = server.accept()
    print(f"New connection from {client_address}")

    # Start a thread for each client and store it in the dictionary.
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_threads[client_socket] = threading.Event()
    client_thread.start()
