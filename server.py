import os
import socket
import struct

host = "localhost"
port = 12000

def send_file(connectedClient, path):
    size = os.path.getsize(path)
    connectedClient.sendall(struct.pack("!Q", size))
    with open(path, "rb") as f:
        while true:
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
    cmd = conn.recv(1024).decode().strip()

    if cmd != "LIST":
        connectedClient.close()
        continue

    base_dir = "sample_files"
    files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    connectedClient.sendall(json.dumps(files).encode())

    requested = conn.recv(1024).decode().strip()
    path = os.path.join(base_dir, requested)

    if not os.path.isfile(filename):
        connectedClient.sendall(struct.pack("!Q", 0))
        connectedClient.close()
        continue

    size = os.path.getsize(filename)
    print(f"File size: {size}")
    connectedClient.sendall(struct.pack("!Q", size))





    connectedClient.close()