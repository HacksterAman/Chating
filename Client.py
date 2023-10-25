import socket
import threading

# Create a client socket.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.148.233', 12345))

# Function to receive and display messages.
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred.")
            client.close()
            break

# Start a thread to receive and display messages.
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main loop to send messages.
while True:
    message = input()
    client.send(message.encode('utf-8'))
