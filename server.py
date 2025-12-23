import socket

host = "127.0.0.1"
port = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((host, port))
serverSocket.listen(1)

while True:
    connectedClient, _ = serverSocket.accept()

    filename = connectedClient.recv(1024).decode().strip()

    if not

