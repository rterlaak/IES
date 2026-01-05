import os
import socket
import struct
import json

host = "127.0.0.1"
port = 12000
base_dir = "sample files"

def send_file(connectedClient, path):
    size = os.path.getsize(path)
    connectedClient.sendall(struct.pack("!Q", size))

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((host, port))
print(f"socket bound to port: {port}")

serverSocket.listen(1)
print("Socket is listening...")

while True:
    connectedClient, clientAddress = serverSocket.accept()
    print("Accepted:", clientAddress)

    try:
        cmd = connectedClient.recv(1024).decode().strip()
        print("CMD:", cmd)

        if cmd != "LIST":
            connectedClient.close()
            continue

        files = [
            f for f in os.listdir(base_dir)
            if os.path.isfile(os.path.join(base_dir, f))
        ]
        connectedClient.sendall(json.dumps(files).encode())

        while True:
            requested = connectedClient.recv(1024).decode().strip()
            path = os.path.join(base_dir, requested)

            if not os.path.isfile(path):
                connectedClient.sendall(struct.pack("!Q", 0))
                continue

            size = os.path.getsize(path)
            print(f"File size: {size}")
            connectedClient.sendall(struct.pack("!Q", size))

            with open(path, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    connectedClient.sendall(chunk)

            break

        connectedClient.close()

    except Exception as e:
        print("Server error:", repr(e))
        try:
            connectedClient.close()
        except:
            pass