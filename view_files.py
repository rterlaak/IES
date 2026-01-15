import os
import socket
import json
import struct


def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError("error in recvall")
        data += part
    return data

def view_files_client(HOST, PORT, LOCAL_DIR):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    print("1 - Show local files")
    print("2 - Show server files")
    sort = input("Choose option: ").strip()

    # ===== LOCAL FILES =====
    if sort == "1":
        if not os.path.isdir(LOCAL_DIR):
            print("Local folder not found")
            clientSocket.close()
            return

        files = [
            f for f in os.listdir(LOCAL_DIR)
            if os.path.isfile(os.path.join(LOCAL_DIR, f))
        ]

        print("Local files:")
        for counter, f in enumerate(files):
            print(counter, ") ", f)

    # ===== SERVER FILES =====
    elif sort == "2":
        clientSocket.sendall(b"LIST")
        files_json = clientSocket.recv(1024).decode()
        files = json.loads(files_json)
        print("Server files:")
        for counter, f in enumerate(files):
            print(counter, ") ", f)
    clientSocket.close()