import os
import socket
import struct
import json

host = "localhost"
port = 12000
local_dir = "local_files"

def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError
        data += part
    return data

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

print("1 - Show local files")
print("2 - Show server files")
choice = input("Choose an option: ").strip()

if choice == "1":
    files = [
        f for f in os.listdir(local_dir)
        if os.path.isfile(os.path.join(local_dir, f))
    ]
    print("Local files: ")
    for f in files:
        print(f)
elif choice == "2":
    clientSocket.sendall(b"LIST")
    files_json = clientSocket.recv(8192).decode()
    files = json.loads(files_json)

    print("Server files: ")
    for f in files:
        print(f)

for i, name in enumerate(files, 1):
    print(f"{i}. {name}")

filename = input("Which file would you like to download:").strip()
clientSocket.sendall(filename.encode())

size = struct.unpack("!Q", recvall(clientSocket, 8))[0]

if size == 0:
    print("File not found")
    clientSocket.close()
    exit()

with open("downloaded_" + filename, "wb") as f:
    remaining = size
    while remaining > 0:
        chunk = clientSocket.recv(4096 if remaining >= 4096 else remaining)
        if not chunk:
            raise ConnectionError
        f.write(chunk)
        remaining -= len(chunk)

clientSocket.close()
print("Download complete")
