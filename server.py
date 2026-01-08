import os
import socket
import struct
import json

host = "localhost"
port = 12000
server_dir = "server_files"

def send_file(connectedClient, path):
    size = os.path.getsize(path)
    connectedClient.sendall(struct.pack("!Q", size))
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            connectedClient.sendall(chunk)


serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((host, port))
print(f"socket bound to port: {port}")

serverSocket.listen(1)
print("Socket is listening...")

while True:
    connectedClient, clientAddress = serverSocket.accept()
    print(f"Connected to: {clientAddress[0]} : {clientAddress[1]}")
    try:
        cmd = connectedClient.recv(1024).decode().strip()
        if cmd != "LIST":
            connectedClient.close()
            continue

        files = [
            f for f in os.listdir(server_dir)
            if os.path.isfile(os.path.join(server_dir, f))
        ]
        connectedClient.sendall(json.dumps(files).encode())

        requested = connectedClient.recv(1024).decode().strip()
        path = os.path.join(server_dir, requested)

        if not os.path.isfile(path):
            connectedClient.sendall(struct.pack("!Q", 0))
            connectedClient.close()
            continue

        send_file(connectedClient, path)

    except Exception as e:
        print("Server error:", repr(e))
        try:
            connectedClient.close()
        except:
            pass


    connectedClient.close()